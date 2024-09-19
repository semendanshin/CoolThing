import re

from fastapi import Form

from domain.dto.campaign import CampaignCreateDTO


def create_campaign_form(
        name: str = Form(...),
        welcome_message: str = Form(...),
        chats: str = Form(...),
        plus_keywords: str = Form(...),
        minus_keywords: str = Form(...),
        gpt_settings_id: str = Form(...),
        scope: str = Form(...),
        campaign_chat_interval_start: int = Form(default=None),
        campaign_chat_interval_end: int = Form(default=None),
        campaign_welcome_wait_start: int = Form(default=None),
        campaign_welcome_wait_end: int = Form(default=None),
) -> CampaignCreateDTO:
    return CampaignCreateDTO(
        name=name,
        welcome_message=welcome_message,
        chats=[chat for chat in re.split(r"\s*,\s*", chats)],
        plus_keywords=[keyword for keyword in re.split(r"\s*,\s*", plus_keywords)],
        minus_keywords=[keyword for keyword in re.split(r"\s*,\s*", minus_keywords)],
        gpt_settings_id=gpt_settings_id,
        scope=scope,
        chat_answer_wait_interval_seconds=(f"{campaign_chat_interval_start}-{campaign_chat_interval_end}"
                                           if campaign_chat_interval_start and campaign_chat_interval_end else None),
        new_lead_wait_interval_seconds=(f"{campaign_welcome_wait_start}-{campaign_welcome_wait_end}"
                                        if campaign_welcome_wait_start and campaign_welcome_wait_end else None),
    )
