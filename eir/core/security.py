import hashlib
import hmac
import secrets
import time
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from pwdlib import PasswordHash

from eir.core.config import settings

password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return password_hasher.verify(password, password_hash)
    except (ValueError, TypeError):
        return False


def create_access_token(user_id: str, role: str) -> str:
    now = datetime.now(timezone.utc)
    expires = now + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {
        "sub": user_id,
        "role": role,
        "iat": now,
        "exp": expires,
        "jti": str(uuid4()),
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
    }
    return jwt.encode(
        payload,
        settings.jwt_secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )

def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.jwt_secret_key.get_secret_value(),
        algorithms=[settings.jwt_algorithm],
        issuer=settings.jwt_issuer,
        audience=settings.jwt_audience,
        options={"require": ["sub", "exp", "iat", "jti", "iss", "aud"]},
    )


def generate_refresh_token() -> str:
    return secrets.token_urlsafe(48)


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_csrf_token() -> str:
    nonce = secrets.token_urlsafe(32)
    secret = settings.jwt_secret_key.get_secret_value().encode("utf-8")
    signature = hmac.new(
        secret, nonce.encode("utf-8"), hashlib.sha256
    ).hexdigest()
    return f"{nonce}.{signature}"


def verify_csrf_token(token: str) -> bool:
    try:
        nonce, supplied_signature = token.rsplit(".", 1)
    except ValueError:
        return False

    secret = settings.jwt_secret_key.get_secret_value().encode("utf-8")
    expected_signature = hmac.new(
        secret, nonce.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(supplied_signature, expected_signature)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def refresh_expiry() -> datetime:
    return utc_now() + timedelta(
        days=settings.refresh_token_expire_days
    )
