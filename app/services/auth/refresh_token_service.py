from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken
from app.util.errors import UnauthorizedError
from app.util.tokens import create_auth_jwt


class RefreshTokenService:
    def __init__(self, session: Session):
        self._session = session

    def refresh_auth_jwt(self, refresh_token_uuid: str) -> str:
        refresh_token = self._session.query(RefreshToken)\
            .filter(RefreshToken.id == refresh_token_uuid).first()
        if not refresh_token:
            raise UnauthorizedError(messagE='Invalid refresh token')

        new_jwt = create_auth_jwt(str(refresh_token.user_id))
        return new_jwt
