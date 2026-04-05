from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user import User
from app.util.errors import NotFoundError


class UsersService:
    def __init__(self, session: Session):
        self._session = session

    def get_user_by_id(self, id: UUID) -> User:
        user = self._session.query(User).filter(User.id == id).first()
        if not user:
            raise NotFoundError(message='User does not exist')
        return user
