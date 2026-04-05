from datetime import datetime
from uuid import UUID

from app.api.schemas.common_schemas import AliasedBaseModel


class MeResponse(AliasedBaseModel):
    id: UUID
    email: str
    first_name: str | None
    last_name: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}
