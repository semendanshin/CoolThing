import logging

from fastapi import APIRouter, Request, HTTPException, Body

from dependencies.usecases.campaign import get_campaigns_usecase
from dependencies.usecases.scripts import get_scripts_use_case
from .common import templates


# included to scripts router
router = APIRouter(
    prefix='/active',
)

logger = logging.getLogger(__name__)


@router.get('')
async def get_active_scripts(request: Request):
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


@router.post('/stop')
async def stop_active_script(
        sfc_id: str = Body(..., embed=True),
):
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


# TODO: write the template
