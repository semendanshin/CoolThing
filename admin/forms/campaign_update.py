import re
from typing import Optional, Literal

from fastapi import Form, Path

from domain.dto.campaign import CampaignUpdateDTO


def update_campaign_form(
    id: str = Path(..., alias="campaign_id"),
    name: str = Form(..., alias="campaign_name"),
    welcome_message: str = Form(default=None),
    chats: str = Form(default=None),
    plus_keywords: str = Form(default=""),
    minus_keywords: str = Form(default=""),
    gpt_settings_id: str = Form(default=None),
    scope: str = Form(...),
    campaign_chat_interval_start: int = Form(default=None),
    campaign_chat_interval_end: int = Form(default=None),
    campaign_welcome_wait_start: int = Form(default=None),
    campaign_welcome_wait_end: int = Form(default=None),
    enabled: bool = Form(default=False),
    type: Literal["Native integration", "Monitoring"] = Form(default=None),
) -> CampaignUpdateDTO:
    return CampaignUpdateDTO(
        id=id,
        name=name,
        welcome_message=welcome_message,
        chats=[chat for chat in re.split(r"\s*,\s*", chats)] if chats else [],
        plus_keywords=[keyword for keyword in re.split(r"\s*,\s*", plus_keywords)],
        minus_keywords=[keyword for keyword in re.split(r"\s*,\s*", minus_keywords)],
        gpt_settings_id=gpt_settings_id,
        scope=scope,
        chat_answer_wait_interval_seconds=(f"{campaign_chat_interval_start}-{campaign_chat_interval_end}"
                                           if campaign_chat_interval_start and campaign_chat_interval_end else None),
        new_lead_wait_interval_seconds=(f"{campaign_welcome_wait_start}-{campaign_welcome_wait_end}"
                                        if campaign_welcome_wait_start and campaign_welcome_wait_end else None),
        type=type if type in ("Monitoring", "Native integration") else None,
        enabled=enabled,
    )
