from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.util.errors import UnauthorizedError
from app.util.tokens import decode_token


security = HTTPBearer(auto_error=False)


def get_req_user_id(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)]):
    if not credentials or credentials.scheme != "Bearer":
        raise UnauthorizedError(message='Not authenticated')

    payload = decode_token(credentials.credentials)
    if not payload or payload.get("type") != "access":
        raise UnauthorizedError(message='Invalid or expired token')

    sub = payload.get("sub")
    if not sub:
        raise UnauthorizedError(message='Invalid token')

    try:
        user_id = UUID(sub)
    except ValueError:
        raise UnauthorizedError(message='Invalid token')

    return user_id
