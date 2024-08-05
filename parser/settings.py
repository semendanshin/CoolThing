import os
import re

from pathlib import Path
from typing import Type, Tuple, Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource, JsonConfigSettingsSource


class Keywords(BaseSettings):
    positive: list[str]
    negative: list[str]


class ParserSettings(BaseSettings):
    keywords: Keywords
    chats: list[str | int]


class AppSettings(BaseSettings):
    id: str
    api_id: int
    api_hash: str
    session_string: str
    proxy: Optional[str] = None

    @field_validator('proxy')
    @classmethod
    def validate_proxy(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None

        protocol_regex = r'^(http|socks4|socks5)://'
        body_regex = r'\w+://(\w+:\w+@)?[\w.-]+:\d+'

        if re.match(body_regex, value):
            if re.match(protocol_regex, value):
                return value
            else:
                raise ValueError('Available protocols: http, socks4, socks5')
        else:
            raise ValueError('Invalid proxy format')


class RabbitSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    vhost: str
    campaign_id: str


class Settings(BaseSettings):
    app: AppSettings
    rabbit: RabbitSettings
    parser: ParserSettings

    debug: bool = False

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
