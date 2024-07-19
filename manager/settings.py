from pathlib import Path
from typing import Type, Tuple

from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource, JsonConfigSettingsSource


class AppSettings(BaseSettings):
    id: str
    api_id: int
    api_hash: str
    session_string: str


class DBSettings(BaseSettings):
    name: str
    user: str
    password: str
    host: str
    port: int


class RabbitSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    vhost: str
    queue: str


class OpenAISettings(BaseSettings):
    api_key: str
    model: str


class Settings(BaseSettings):
    app: AppSettings
    rabbit: RabbitSettings
    openai: OpenAISettings
    db: DBSettings

    welcome_message: str
    campaign_id: str

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
