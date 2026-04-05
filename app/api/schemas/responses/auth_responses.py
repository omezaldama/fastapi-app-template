from app.api.schemas.common_schemas import AliasedBaseModel


class LoginResponse(AliasedBaseModel):
    token: str


class RefreshTokenResponse(AliasedBaseModel):
    token: str
