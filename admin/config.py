from pathlib import Path
from urllib.parse import quote_plus
from typing import Type, Tuple

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource, JsonConfigSettingsSource


class DBSettings(BaseSettings):
    host: str
    port: int
    name: str
    user: str
    password: SecretStr

    @property
    def url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}"


class ScriptsDBSettings(BaseSettings):
    user: str
    password: SecretStr
    host: str
    port: int
    name: str

    def __post_init__(self):
        self.password = SecretStr(quote_plus(self.password.get_secret_value()))
        self.user =quote_plus(self.user)

    @property
    def url(self):
        return f"mongodb://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/"


class AuthSettings(BaseSettings):
    code: SecretStr
    secret_key: SecretStr
    access_token_lifetime_seconds: int = 60 * 60


class MQSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    vhost: str

    @property
    def url(self):
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/{self.vhost}"


class Settings(BaseSettings):
    db: DBSettings
    scripts_db: ScriptsDBSettings
    auth: AuthSettings
    mq: MQSettings

    debug: bool = True

    model_config = SettingsConfigDict(
        extra='ignore',
        json_file=Path(__file__).parent / 'settings.json',
        json_file_encoding='utf-8',
    )

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (JsonConfigSettingsSource(settings_cls),)


settings = Settings()
