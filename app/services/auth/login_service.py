from typing import Tuple

from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.services.schemas.auth_schemas import LoginData
from app.util.errors import UnauthorizedError
from app.util.password import verify_password
from app.util.tokens import create_auth_jwt, create_refresh_jwt


class LoginService:
    def __init__(self, session: Session):
        self._session = session

    def login(self, login_data: LoginData) -> Tuple[str, str]:
        user = self._session.query(User).filter(User.email == login_data.email).first()
        if not user:
            raise UnauthorizedError()
        if not verify_password(login_data.password, user.hashed_password):
            raise UnauthorizedError()

        refresh_token = RefreshToken(user_id=user.id)

        self._session.add(refresh_token)
        self._session.commit()
        self._session.refresh(refresh_token)

        auth_jwt = create_auth_jwt(str(user.id))
        refresh_jwt = create_refresh_jwt(str(refresh_token.id))

        return auth_jwt, refresh_jwt
