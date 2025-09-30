from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):

    bot_token: SecretStr
    secret: SecretStr
    access_password: SecretStr

    login: str
    password: SecretStr

    digit: int
    period: int

    tg_admin_id: int
    created_at: int

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config = Settings()
