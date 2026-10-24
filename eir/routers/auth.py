import hmac

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from eir.core.config import settings
from eir.core.security import create_csrf_token, verify_csrf_token
from eir.db.sessions import get_db
from eir.schemas.auth import (
    LoginRequest,
    PatientRegister,
    TokenResponse,
    UserResponse,
)
from eir.services.auth_service import (
    login_user,
    register_user,
    revoke_refresh_token,
    rotate_refresh_token,
)
from eir.services.error.auth import (
    AuthServiceError,
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    InvalidRefreshTokenError,
    PatientNotFoundError,
    RefreshTokenReuseError,)

router = APIRouter(prefix="/auth", tags=["Authentication"])


def set_auth_cookies(
    response: Response,
    refresh_token: str,
    csrf_token: str,
) -> None:
    max_age = settings.refresh_token_expire_days * 24 * 60 * 60

    response.set_cookie(
        key=settings.refresh_cookie_name,
        value=refresh_token,
        max_age=max_age,
        httponly=True,
        secure=settings.refresh_cookie_secure,
        samesite=settings.refresh_cookie_samesite,
        path="/auth",
    )

    response.set_cookie(
        key=settings.csrf_cookie_name,
        value=csrf_token,
        max_age=max_age,
        httponly=False,
        secure=settings.refresh_cookie_secure,
        samesite=settings.refresh_cookie_samesite,
        path="/auth",
    )


def clear_auth_cookies(response: Response) -> None:
    response.delete_cookie(
        key=settings.refresh_cookie_name,
        path="/auth",
        secure=settings.refresh_cookie_secure,
        httponly=True,
        samesite=settings.refresh_cookie_samesite,
    )

    response.delete_cookie(
        key=settings.csrf_cookie_name,
        path="/auth",
        secure=settings.refresh_cookie_secure,
        httponly=False,
        samesite=settings.refresh_cookie_samesite,
    )


def require_valid_csrf(request: Request) -> None:
    csrf_cookie = request.cookies.get(settings.csrf_cookie_name)
    csrf_header = request.headers.get(settings.csrf_header_name)

    if not csrf_cookie or not csrf_header:
        raise HTTPException(
            status_code=403,
            detail="CSRF token is missing",
        )

    if not hmac.compare_digest(csrf_cookie, csrf_header):
        raise HTTPException(
            status_code=403,
            detail="CSRF token mismatch",
        )

    if not verify_csrf_token(csrf_header):
        raise HTTPException(
            status_code=403,
            detail="Invalid CSRF token",
        )


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    data: PatientRegister,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    try:
        user = await register_user(
            email=str(data.email),
            password=data.password,
            patient_id=data.patient_id,
            db=db,
        )
    except EmailAlreadyExistsError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except PatientNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return UserResponse.model_validate(user)


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    try:
        user, access_token, refresh_token = await login_user(
            email=str(data.email),
            password=data.password,
            db=db,
        )
    except InvalidCredentialsError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc

    csrf_token = create_csrf_token()
    set_auth_cookies(response, refresh_token, csrf_token)

    return TokenResponse(
        access_token=access_token,
        csrf_token=csrf_token,
        user=UserResponse.model_validate(user),
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    require_valid_csrf(request)

    raw_token = request.cookies.get(settings.refresh_cookie_name)

    if not raw_token:
        raise HTTPException(
            status_code=401,
            detail="Refresh token is missing",
        )

    try:
        user, access_token, new_refresh_token = await rotate_refresh_token(
            raw_token=raw_token,
            db=db,
        )
    except (InvalidRefreshTokenError, RefreshTokenReuseError) as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except AuthServiceError as exc:
        raise HTTPException(status_code=401, detail="Authentication failed") from exc

    new_csrf_token = create_csrf_token()
    set_auth_cookies(response, new_refresh_token, new_csrf_token)

    return TokenResponse(
        access_token=access_token,
        csrf_token=new_csrf_token,
        user=UserResponse.model_validate(user),
    )


@router.post("/logout", status_code=204)
async def logout(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> Response:
    require_valid_csrf(request)

    raw_token = request.cookies.get(settings.refresh_cookie_name)

    if raw_token:
        await revoke_refresh_token(raw_token, db)

    clear_auth_cookies(response)
    response.status_code = 204
    return response