from typing import Optional

from pydantic import BaseModel, Field


class SetTargetChatsRequest(BaseModel):
    process_id: str
    target_chats: list[str]


class SetScriptStatusRequest(BaseModel):
    process_id: str
    is_successful: bool


class SetMessageStatusRequest(BaseModel):
    process_id: str
    message_id: str
    is_sent: bool

    text: Optional[str] = None


class SetChatStatusRequest(BaseModel):
    process_id: str
    chat_link: str
    is_successful: bool

    on_message: Optional[str] = Field(default=None, exclude=True)
    reason: Optional[str] = Field(default=None, exclude=True)
