from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from abstractions.usecases.CampaingsUseCaseInterface import CampaignsUseCaseInterface
from dependencies.usecases.campaign import get_campaigns_usecase
from domain.dto.campaign import CampaignUpdateDTO
from forms.campaign_update import update_campaign_form

router = APIRouter(
    prefix="/campaigns",
    tags=["campaigns"],
)

templates = Jinja2Templates(directory='templates')


@router.get("")
async def get_campaigns(
        request: Request,
        campaigns: CampaignsUseCaseInterface = Depends(get_campaigns_usecase)
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="campaigns.html",
        context={
            'campaigns': await campaigns.get_campaigns(),
        }
    )


@router.get("/{campaign_id}")
async def get_campaign(
        campaign_id: str,
        request: Request,
        campaigns: CampaignsUseCaseInterface = Depends(get_campaigns_usecase)
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="campaign.html",
        context={
            'campaign': await campaigns.get_campaign(campaign_id=campaign_id),
        }
    )


@router.post("/{campaign_id}")
async def update_campaign(
        campaign_id: str,
        update_schema: CampaignUpdateDTO = Depends(update_campaign_form),
        campaigns: CampaignsUseCaseInterface = Depends(get_campaigns_usecase)
) -> RedirectResponse:
    await campaigns.update_campaign(campaign_id=campaign_id, schema=update_schema)
    return RedirectResponse(url=f'/campaigns/{campaign_id}', status_code=303)
