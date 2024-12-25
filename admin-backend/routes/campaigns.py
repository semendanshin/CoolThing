import logging
from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette.responses import JSONResponse

from abstractions.usecases.CampaingsUseCaseInterface import CampaignsUseCaseInterface
from dependencies.usecases.campaign import get_campaigns_usecase
from domain.dto.campaign import CampaignCreateDTO, CampaignUpdateDTO
from domain.models import Campaign as CampaignModel

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/campaigns",
    tags=["campaigns"],
)


class Campaign(BaseModel):
    id: UUID
    welcome_message: str
    chats: list[str]
    plus_keywords: list[str]
    minus_keywords: list[str]
    gpt_settings_id: str
    scope: str
    chat_answer_wait_interval_seconds: str
    new_lead_wait_interval_seconds: str
    updated_at: datetime
    created_at: datetime

    @classmethod
    def from_domain(cls, model: CampaignModel) -> "Campaign":
        return Campaign(
            id=UUID(model.id),
            welcome_message=model.welcome_message,
            chats=model.chats,
            plus_keywords=model.plus_keywords,
            minus_keywords=model.minus_keywords,
            gpt_settings_id=model.gpt_settings_id,
            scope=model.scope,
            chat_answer_wait_interval_seconds=model.chat_answer_wait_interval_seconds,
            new_lead_wait_interval_seconds=model.new_lead_wait_interval_seconds,
            updated_at=model.updated_at,
            created_at=model.created_at,
        )


@router.get("")
async def get_campaigns(
        campaigns_use_case: CampaignsUseCaseInterface = Depends(get_campaigns_usecase)
) -> list[Campaign]:
    campaigns = await campaigns_use_case.get_campaigns()
    result = list(map(lambda c: Campaign.from_domain(c), campaigns))
    return result


class CampaignCreateRequest(BaseModel):
    welcome_message: str
    chats: list[str]
    plus_keywords: list[str]
    minus_keywords: list[str]
    gpt_settings_id: str
    scope: str
    chat_answer_wait_interval_seconds: str
    new_lead_wait_interval_seconds: str


@router.get("/{campaign_id}")
async def get_campaign(
        campaign_id: str,
        campaigns_use_case: CampaignsUseCaseInterface = Depends(get_campaigns_usecase)
) -> Campaign:
    campaign = await campaigns_use_case.get_campaign(campaign_id)
    result = Campaign.from_domain(campaign)
    return result


@router.post("")
async def create_campaign(
        campaign_create: CampaignCreateRequest,
        campaigns_use_case: CampaignsUseCaseInterface = Depends(get_campaigns_usecase)
) -> Campaign:
    campaign = await campaigns_use_case.create(CampaignCreateDTO(**campaign_create.model_dump()))
    result = Campaign.from_domain(campaign)
    return result


class CampaignUpdateRequest(BaseModel):
    welcome_message: str
    chats: list[str]
    plus_keywords: list[str]
    minus_keywords: list[str]
    gpt_settings_id: Optional[str]
    scope: str
    chat_answer_wait_interval_seconds: str
    new_lead_wait_interval_seconds: str


@router.put("/{campaign_id}")
async def update_campaign(
        campaign_id: str,
        dto: CampaignUpdateRequest,
        campaigns_use_case: CampaignsUseCaseInterface = Depends(get_campaigns_usecase)
) -> Campaign:
    campaign = await campaigns_use_case.update(campaign_id, CampaignUpdateDTO(id=campaign_id, **dto.model_dump()))
    result = Campaign.from_domain(campaign)
    return result


@router.delete("/{campaign_id}")
async def delete_campaign(
        campaign_id: str,
        campaigns_use_case: CampaignsUseCaseInterface = Depends(get_campaigns_usecase)
):
    await campaigns_use_case.delete(campaign_id)
