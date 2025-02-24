from datetime import datetime
from pathlib import Path
from typing import Type, Tuple
from urllib.parse import quote_plus
from uuid import UUID

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource, JsonConfigSettingsSource


class ScriptsDBSettings(BaseSettings):
    user: str
    password: SecretStr
    host: str
    port: int
    name: str

    def __post_init__(self):
        self.password = SecretStr(quote_plus(self.password.get_secret_value()))
        self.user = quote_plus(self.user)

    @property
    def url(self):
        return f"mongodb://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}?authSource=admin&directConnection=true"


class DelaySettings(BaseSettings):
    typing_and_sending_sleep_from: int
    typing_and_sending_sleep_to: int


class ScriptsSettings(BaseSettings):
    interval_seconds: int


class MQSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    vhost: str

    @property
    def url(self):
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/{self.vhost}"


class DBSettings(BaseSettings):
    host: str
    port: int
    name: str
    user: str
    password: SecretStr

    @property
    def url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}"


class WatcherSettings(BaseSettings):
    base_url: str
    new_activation_endpoint: str
    target_chats_endpoint: str
    script_status_endpoint: str
    chat_status_endpoint: str
    message_status_endpoint: str


class NotifierSettings(BaseSettings):
    base_url: str


class ScriptToPerform(BaseSettings):
    id: str
    script_for_campaign_id: str
    created_at: datetime


class Settings(BaseSettings):
    scripts_db: ScriptsDBSettings
    mq: MQSettings
    db: DBSettings
    watcher: WatcherSettings
    notifier: NotifierSettings
    script_to_perform: ScriptToPerform

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
