from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel


class Message(BaseModel):
    text: str
    sent_at: datetime
    type: Literal["outcome", "income"]


class ChatInfo(BaseModel):
    chat_id: str
    bot_nickname: str
    user_nickname: str
    user_id: Optional[str] = None
    last_message: str
    status: Literal["online", "offline"]


class Chat(BaseModel):
    info: ChatInfo
    messages: list[Message]
