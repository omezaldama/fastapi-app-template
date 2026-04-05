from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken


class LogoutService:
    def __init__(self, session: Session):
        self._session = session

    def logout(self, refresh_token_id: str):
        self._session.query(RefreshToken)\
            .filter(RefreshToken.id == refresh_token_id).delete()
        self._session.commit()
