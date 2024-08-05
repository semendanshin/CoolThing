from pathlib import Path
from typing import Type, Tuple, Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource, JsonConfigSettingsSource

import re


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


class OpenAISettings(BaseSettings):
    api_key: str
    model: str
    proxy: Optional[str] = None
    assistant: Optional[str] = None
    service_prompt: Optional[str] = None

    @field_validator('proxy')
    @classmethod
    def validate_proxy(cls, value: Optional[str]) -> Optional[str]:
        if value:
            # proxy is protocol://host:port or protocol://user:password@host:port
            protocol_regex = r'^(http|https|socks5)://'
            body_regex = r'\w+://(\w+:\w+@)?[\w.-]+:\d+'

            # check body first to avoid unnecessary regex matching
            if re.match(body_regex, value):
                if re.match(protocol_regex, value):
                    return value
                else:
                    raise ValueError('Available protocols: http, https, socks5')
            else:
                raise ValueError('Invalid proxy format')

        return None


class Settings(BaseSettings):
    app: AppSettings
    rabbit: RabbitSettings
    openai: OpenAISettings
    db: DBSettings

    welcome_message: str
    campaign_id: str

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
