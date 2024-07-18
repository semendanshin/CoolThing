import os

from pathlib import Path
from typing import Type, Tuple

from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource, JsonConfigSettingsSource


class Keywords(BaseSettings):
    positive: list[str]
    negative: list[str]


class ParserSettings(BaseSettings):
    keywords: Keywords
    chats: list[int]


class AppSettings(BaseSettings):
    id: str
    api_id: int
    api_hash: str
    session_string: str


class RabbitSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    vhost: str
    queue: str


class Settings(BaseSettings):
    app: AppSettings
    rabbit: RabbitSettings
    parser: ParserSettings

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
