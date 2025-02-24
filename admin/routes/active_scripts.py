import logging
from uuid import UUID

from fastapi import APIRouter, Request, HTTPException, Body
from starlette.responses import HTMLResponse

from dependencies.usecases.campaign import get_campaigns_usecase
from dependencies.usecases.scripts import get_scripts_use_case
from domain.models import ActiveScriptProcess
from .common import templates

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/active',
)


# GET All Active Scripts
@router.get('')
async def get_active_scripts(request: Request):
    """
    Render a page with all active scripts.
    """
    scripts_service = get_scripts_use_case()
    campaigns_service = get_campaigns_usecase()

    active_scripts = await scripts_service.get_active_scripts()
    scripts = await scripts_service.get_scripts()
    campaigns = await campaigns_service.get_campaigns()

    # mappings for easy client-side lookup
    scripts_dict = {script.id: script.name for script in scripts}
    campaigns_dict = {campaign.id: campaign.name for campaign in campaigns}

    return templates.TemplateResponse(
        request=request,
        name='active_scripts.html',
        context={
            'active_scripts': active_scripts,
            'scripts_dict': scripts_dict,
            'campaigns_dict': campaigns_dict,
        },
    )


# POST Stop a Script by Campaign ID
@router.post('/stop')
async def stop_active_script(
        sfc_id: str = Body(..., embed=True),
):
    """
    Stop an active script by campaign ID.
    """
    service = get_scripts_use_case()
    try:
        success = await service.stop_script(sfc_id=sfc_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"No active scripts with id {sfc_id}")

    except Exception:
        logger.error('Something went wrong during script stopping', exc_info=True)
        raise HTTPException(
            status_code=500,
            detail='Something went wrong during script stopping'
        )


@router.get('/{sfc_id}')
async def get_active_script(
        sfc_id: str,
        request: Request,
) -> HTMLResponse:
    scripts_service = get_scripts_use_case()
    campaigns_service = get_campaigns_usecase()

    active_script_process = await scripts_service.get_active_script_by_sfc(sfc_id)
    sfc = await scripts_service.get_sfc(sfc_id=sfc_id)
    campaign = await campaigns_service.get_campaign(sfc.campaign_id)

    return templates.TemplateResponse(
        request=request,
        name='active_script.html',
        context={
            'process': active_script_process,
            'sfc': sfc,
            'campaign': campaign,
        }
    )


# GET Single Active Script Process Details
@router.get('/{process_id}/entity')
async def get_single_active_script(
        process_id: UUID,
) -> ActiveScriptProcess:
    """
    Fetch details of a single active script process.
    """
    service = get_scripts_use_case()
    process = await service.get_active_script(str(process_id))
    if not process:
        raise HTTPException(status_code=404, detail=f"No active script with id {process_id}")

    return process
