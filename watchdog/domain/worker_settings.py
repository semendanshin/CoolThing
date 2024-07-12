from dataclasses import dataclass


# @dataclass
# class RabbitSettings:
#     host: str
#     port: int
#     user: str
#     password: str
#     vhost: str
#     queue: str
#
#
# @dataclass
# class AppSettings:
#     api_id: int
#     api_hash: str
#     session_string: str
#
#
# @dataclass
# class WorkerSettings:
#     app: AppSettings
#     rabbit: RabbitSettings
#
#
# @dataclass
# class ParserSettings(WorkerSettings):
#     pass
#
#
# @dataclass
# class ManagerSettings(WorkerSettings):
#     pass























@dataclass
class Worker:
    id: str
    app_id: str
    app_hash: str
    session_string: str
    proxy: str

    campaign_id: str
    role: str
    status: str


@dataclass
class GPT:
    model: str
    assistant: str
    token: str


@dataclass
class Campaign:
    id: str
    welcome_message: str
    chats: list[str]
    plus_keywords: list[str]
    minus_keywords: list[str]
    gpt_settings: GPT
    topic: str


@dataclass
class Chat:
    id: str
    campaign_id: str
    worker_id: str
    username: str
    status: str
    lead_message: str
    lead_chat_id: str


@dataclass
class Message:
    id: str
    chat_id: str
    text: str
    is_outgoing: bool










