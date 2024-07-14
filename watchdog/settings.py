from pathlib import Path
from typing import Type, Tuple

from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource, JsonConfigSettingsSource


class DBSettings(BaseSettings):
    name: str
    user: str
    password: str
    host: str
    port: int


class WatchdogSettings(BaseSettings):
    interval_seconds: int


class RabbitSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    vhost: str


class Settings(BaseSettings):
    db: DBSettings
    watchdog: WatchdogSettings
    rabbit: RabbitSettings

    debug: bool = False

    model_config = SettingsConfigDict(
        extra='allow',
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
