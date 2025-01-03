import re

from fastapi import Form, Path

from domain.dto.campaign import CampaignUpdateDTO


def update_campaign_form(
    id: str = Path(..., alias="campaign_id"),
    welcome_message: str = Form(alias="campaign_welcome_message"),
    chats: str = Form(alias="campaign_chats"),
    plus_keywords: str = Form(alias="campaign_plus_keywords"),
    minus_keywords: str = Form(alias="campaign_minus_keywords"),
    gpt_settings_id: str = Form(alias="campaign_gpt_settings_id"),
    scope: str = Form(alias="campaign_scope"),
    campaign_chat_interval_start: int = Form(...),
    campaign_chat_interval_end: int = Form(...),
    campaign_welcome_wait_start: int = Form(...),
    campaign_welcome_wait_end: int = Form(...),
) -> CampaignUpdateDTO:
    return CampaignUpdateDTO(
        id=id,
        welcome_message=welcome_message,
        chats=[chat for chat in re.split(r"\s*,\s*", chats)],
        plus_keywords=[keyword for keyword in re.split(r"\s*,\s*", plus_keywords)],
        minus_keywords=[keyword for keyword in re.split(r"\s*,\s*", minus_keywords)],
        gpt_settings_id=gpt_settings_id,
        scope=scope,
        chat_answer_wait_interval_seconds=f"{campaign_chat_interval_start}-{campaign_chat_interval_end}",
        new_lead_wait_interval_seconds=f"{campaign_welcome_wait_start}-{campaign_welcome_wait_end}",
    )
