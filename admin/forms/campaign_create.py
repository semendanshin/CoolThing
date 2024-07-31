import re

from fastapi import Form

from domain.dto.campaign import CampaignCreateDTO


def create_campaign_form(
    welcome_message: str = Form(...),
    chats: str = Form(...),
    plus_keywords: str = Form(...),
    minus_keywords: str = Form(...),
    gpt_settings_id: str = Form(...),
    scope: str = Form(...),
) -> CampaignCreateDTO:
    return CampaignCreateDTO(
        welcome_message=welcome_message,
        chats=[chat for chat in re.split(r"\s*,\s*", chats)],
        plus_keywords=[keyword for keyword in re.split(r"\s*,\s*", plus_keywords)],
        minus_keywords=[keyword for keyword in re.split(r"\s*,\s*", minus_keywords)],
        gpt_settings_id=gpt_settings_id,
        scope=scope,
    )
