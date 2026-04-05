from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from app.config import settings
from app.util.errors import UnauthorizedError


REFRESH_KEY = '__eh_refresh'


def create_jwt(subject: str, ttl: timedelta, type: str) -> str:
    expire = datetime.now(timezone.utc) + ttl
    to_encode = {'sub': subject, 'exp': expire, 'type': type}
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

def create_auth_jwt(subject: str) -> str:
    ttl = timedelta(minutes=settings.access_token_expire_minutes)
    return create_jwt(subject=subject, ttl=ttl, type='access')


def create_refresh_jwt(subject: str | int) -> str:
    ttl = timedelta(days=settings.refresh_token_expire_days)
    return create_jwt(subject=subject, ttl=ttl, type='refresh')


def decode_token(token: str) -> dict[str, Any] | None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None


def get_refresh_token_id(refresh_cookie: str | None) -> str:
    if not refresh_cookie:
        raise UnauthorizedError(message='Invalid refresh token')
    
    refresh_jwt = decode_token(refresh_cookie)
    if not refresh_jwt or refresh_jwt.get("type") != "refresh":
        raise UnauthorizedError(message='Invalid refresh token')

    refresh_token_id = refresh_jwt.get('sub')
    if not refresh_token_id:
        raise UnauthorizedError(message='Invalid refresh token')

    return refresh_token_id
