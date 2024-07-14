from dataclasses import dataclass


@dataclass(kw_only=True)
class WorkerSettings:
    id: str
    app_id: str
    app_hash: str
    session_string: str
    proxy: str
    campaign_id: str
    role: str
    status: str


@dataclass(kw_only=True)
class ManagerSettings(WorkerSettings):
    model: str
    assistant: str
    token: str
    welcome_message: str
    topic: str


@dataclass(kw_only=True)
class ParserSettings(WorkerSettings):
    chats: list[str]
    plus_keywords: list[str]
    minus_keywords: list[str]
    topic: str


@dataclass
class RabbitMQSettings:
    host: str
    port: int
    user: str
    password: str
    vhost: str
