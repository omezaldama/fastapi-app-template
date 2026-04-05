from datetime import datetime
import uuid

from sqlalchemy import DateTime, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, Relationship, mapped_column

from app.db.base import Base
from app.util.datetimes import utc_now


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[uuid.UUID] = mapped_column(Uuid(), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(),
        ForeignKey('app_user.id', ondelete='CASCADE'),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)
