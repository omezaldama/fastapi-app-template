from pydantic import EmailStr, Field

from app.api.schemas.common_schemas import AliasedBaseModel


class SignupRequest(AliasedBaseModel):
    email: EmailStr
    first_name: str | None = Field(default=None, max_length=50)
    last_name: str | None = Field(default=None, max_length=50)
    password: str


class LoginRequest(AliasedBaseModel):
    email: EmailStr
    password: str
