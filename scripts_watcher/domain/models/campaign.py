from typing import Optional, Literal

from domain.models.base import Model


class Campaign(Model):
    # welcome_message: str
    chats: list[str]
    # plus_keywords: list[str]
    # minus_keywords: list[str]
    # gpt_settings_id: str
    # scope: str
    chat_answer_wait_interval_seconds: str
    # new_lead_wait_interval_seconds: Optional[str]

    enabled: Optional[bool]
    type: Optional[Literal["Native integration", "Monitoring"]]
