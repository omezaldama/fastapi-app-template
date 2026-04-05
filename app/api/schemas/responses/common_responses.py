from typing import Any

from app.api.schemas.common_schemas import AliasedBaseModel


class SuccessResponse[T](AliasedBaseModel):
    data: T = None
    message: str = ''
    code: int = 200
    subcode: int = 0


class FailResponse(AliasedBaseModel):
    errors: Any = 'Internal error. Try again later'
    message: str = ''
    code: int = 500
    subcode: int = 0
