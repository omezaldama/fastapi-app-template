from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    algorithm: str = 'HS256'
    access_token_expire_minutes: int
    refresh_token_expire_days: int = 7

    database_url: str

    debug_mode: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
