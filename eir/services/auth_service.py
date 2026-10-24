from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import uuid4
from eir.services.error.auth import (
EmailAlreadyExistsError,
InvalidRefreshTokenError,
PatientNotFoundError,
RefreshTokenReuseError,
InvalidCredentialsError,
)
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from eir.core.security import (
    create_access_token,
    generate_refresh_token,
    hash_password,
    hash_refresh_token,
    refresh_expiry,
    utc_now,
    verify_password,
)
from eir.models.patients import Patient
from eir.models.refresh_tokens import RefreshToken
from eir.models.users import User
from eir.models.enum import UserRole

async def register_user(
    email: str,
    password: str,
    patient_id: str,
    db: AsyncSession,
) -> User:
    normalized_email = email.strip().lower()

    existing_user = await db.execute(
        select(User).where(User.email == normalized_email)
    )
    if existing_user.scalar_one_or_none():
        raise EmailAlreadyExistsError("Email is already registered")

    patient_result = await db.execute(
        select(Patient).where(Patient.patient_id == patient_id)
    )
    patient = patient_result.scalar_one_or_none()

    if patient is None:
        raise PatientNotFoundError("Patient does not exist")

    user = User(
        email=normalized_email,
        password_hash=hash_password(password),
        role=UserRole.PATIENT,
        patient_id=patient_id,
        is_active=True,
    )

    db.add(user)

    try:
        await db.commit()
        await db.refresh(user)
    except IntegrityError as exc:
        await db.rollback()
        raise EmailAlreadyExistsError(
            "Email is already registered"
        ) from exc

    return user


async def login_user(
    email: str,
    password: str,
    db: AsyncSession,
) -> tuple[User, str, str]:
    normalized_email = email.strip().lower()

    result = await db.execute(
        select(User).where(User.email == normalized_email)
    )
    user = result.scalar_one_or_none()

    if (
        user is None
        or not verify_password(password, user.password_hash)
        or not user.is_active
    ):
        raise InvalidCredentialsError("Invalid email or password")

    raw_refresh_token = generate_refresh_token()

    refresh_record = RefreshToken(
        user_id=user.user_id,
        family_id=str(uuid4()),
        token_hash=hash_refresh_token(raw_refresh_token),
        expires_at=refresh_expiry(),
    )

    db.add(refresh_record)
    await db.commit()

    access_token = create_access_token(
        user_id=user.user_id,
        role=user.role.value,
    )

    return user, access_token, raw_refresh_token


async def rotate_refresh_token(
    raw_token: str,
    db: AsyncSession,
) -> tuple[User, str, str]:
    token_hash = hash_refresh_token(raw_token)

    result = await db.execute(
        select(RefreshToken)
        .where(RefreshToken.token_hash == token_hash)
        .with_for_update()
    )
    current_token = result.scalar_one_or_none()

    if current_token is None:
        raise InvalidRefreshTokenError("Invalid refresh token")

    if current_token.revoked_at is not None:
        family_result = await db.execute(
            select(RefreshToken)
            .where(
                RefreshToken.family_id == current_token.family_id,
                RefreshToken.revoked_at.is_(None),
            )
            .with_for_update()
        )

        for token_record in family_result.scalars().all():
            token_record.revoked_at = utc_now()

        await db.commit()
        raise RefreshTokenReuseError(
            "Refresh token reuse detected; session revoked"
        )

    if current_token.expires_at <= utc_now():
        current_token.revoked_at = utc_now()
        await db.commit()
        raise InvalidRefreshTokenError("Refresh token has expired")

    user_result = await db.execute(
        select(User).where(User.user_id == current_token.user_id)
    )
    user = user_result.scalar_one_or_none()

    if user is None or not user.is_active:
        current_token.revoked_at = utc_now()
        await db.commit()
        raise InvalidRefreshTokenError("User is unavailable")

    new_raw_token = generate_refresh_token()

    replacement = RefreshToken(
        user_id=current_token.user_id,
        family_id=current_token.family_id,
        token_hash=hash_refresh_token(new_raw_token),
        expires_at=refresh_expiry(),
    )

    # Revoke the old token and create its replacement.
    current_token.revoked_at = utc_now()
    db.add(replacement)

    try:
        await db.flush()
        current_token.replaced_by_id = replacement.token_id
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    new_access_token = create_access_token(
        user_id=user.user_id,
        role=user.role.value,
    )

    return user, new_access_token, new_raw_token


async def revoke_refresh_token(
    raw_token: str,
    db: AsyncSession,
) -> None:
    token_hash = hash_refresh_token(raw_token)

    result = await db.execute(
        select(RefreshToken)
        .where(RefreshToken.token_hash == token_hash)
        .with_for_update()
    )
    token_record = result.scalar_one_or_none()

    if token_record is not None and token_record.revoked_at is None:
        token_record.revoked_at = utc_now()
        await db.commit()