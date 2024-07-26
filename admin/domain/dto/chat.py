from dataclasses import dataclass


@dataclass(kw_only=True)
class ChatCreateDTO:
    campaign_id: str
    telegram_chat_id: int
    worker_id: str
    username: str
    status: str
    lead_message: str
    lead_chat_id: str


@dataclass(kw_only=True)
class ChatUpdateDTO:
    campaign_id: str
    telegram_chat_id: int
    worker_id: str
    username: str
    status: str
    lead_message: str
    lead_chat_id: str
