from pydantic import BaseModel


class SignupData(BaseModel):
    email: str
    first_name: str | None
    last_name: str | None
    password: str


class LoginData(BaseModel):
    email: str
    password: str
