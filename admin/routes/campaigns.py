from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from abstractions.usecases.CampaingsUseCaseInterface import CampaignsUseCaseInterface
from abstractions.usecases.GPTSettingsUseCaseInterface import GPTSettingsUseCaseInterface
from dependencies.usecases.campaign import get_campaigns_usecase
from dependencies.usecases.gpt_settings import get_gpt_settings_usecase
from domain.dto.campaign import CampaignUpdateDTO, CampaignCreateDTO
from forms.campaign_create import create_campaign_form
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
    campaigns_list = await campaigns.get_campaigns()
    return templates.TemplateResponse(
        request=request,
        name="campaigns.html",
        context={
            'campaigns': campaigns_list,
        }
    )


@router.get("/new")
async def get_new_campaign(
        request: Request,
        gpt_settings: GPTSettingsUseCaseInterface = Depends(get_gpt_settings_usecase),
) -> HTMLResponse:
    gpt_settings_list = await gpt_settings.get_all()
    return templates.TemplateResponse(
        request=request,
        name="new_campaign.html",
        context={
            'gpt_settings': gpt_settings_list,
        }
    )


@router.get("/{campaign_id}")
async def get_campaign(
        campaign_id: str,
        request: Request,
        campaigns: CampaignsUseCaseInterface = Depends(get_campaigns_usecase),
        gpt_settings: GPTSettingsUseCaseInterface = Depends(get_gpt_settings_usecase),
) -> HTMLResponse:
    campaign = await campaigns.get_campaign(campaign_id=campaign_id)
    gpt_settings_list = await gpt_settings.get_all()
    return templates.TemplateResponse(
        request=request,
        name="campaign.html",
        context={
            'campaign': campaign,
            'gpt_settings': gpt_settings_list,
            'delete_url': f"/campaigns/{campaign.id}",
        }
    )


@router.post("/{campaign_id}")
async def update_campaign_backend(
        campaign_id: str,
        update_schema: CampaignUpdateDTO = Depends(update_campaign_form),
        campaigns: CampaignsUseCaseInterface = Depends(get_campaigns_usecase)
) -> RedirectResponse:
    await campaigns.update(campaign_id=campaign_id, schema=update_schema)
    return RedirectResponse(url=f'/campaigns/{campaign_id}', status_code=303)


@router.delete("/{campaign_id}")
async def delete_campaign_backend(
        campaign_id: str,
        campaigns: CampaignsUseCaseInterface = Depends(get_campaigns_usecase)
) -> RedirectResponse:
    await campaigns.delete(campaign_id=campaign_id)
    return RedirectResponse(url=f'/campaigns', status_code=303)


@router.post("")
async def create_campaign_backend(
        create_schema: CampaignCreateDTO = Depends(create_campaign_form),
        campaigns: CampaignsUseCaseInterface = Depends(get_campaigns_usecase)
) -> RedirectResponse:
    await campaigns.create(create_schema)
    return RedirectResponse(url=f'/campaigns', status_code=303)
