from sqlalchemy.orm import Session

from app.models.user import User
from app.services.schemas.auth_schemas import SignupData
from app.util.errors import ConflictError
from app.util.password import hash_password


class SignupService:
    def __init__(self, session: Session):
        self._session = session

    def signup(self, signup_data: SignupData):
        existing_user = self._session.query(User)\
            .filter(User.email == signup_data.email).first()

        if existing_user:
            raise ConflictError(message='User already exists')

        new_user = User(
            email=signup_data.email,
            hashed_password=hash_password(signup_data.password),
            first_name=signup_data.first_name,
            last_name=signup_data.last_name,
        )
        self._session.add(new_user)
        self._session.commit()
        self._session.refresh(new_user)
