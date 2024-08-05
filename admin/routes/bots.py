from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException

from abstractions.usecases.CampaingsUseCaseInterface import CampaignsUseCaseInterface
from dependencies.usecases.bots import get_bots_usecase
from abstractions.usecases.BotsUseCaseInterface import BotsUseCaseInterface
from dependencies.usecases.campaign import get_campaigns_usecase

router = APIRouter(
    prefix='/bots',
    tags=['Bots'],
)

templates = Jinja2Templates(directory='templates')


@router.get("/")
async def get_bots(
        request: Request,
        bots: BotsUseCaseInterface = Depends(get_bots_usecase),
        campaigns: CampaignsUseCaseInterface = Depends(get_campaigns_usecase),
) -> HTMLResponse:
    # match role:
    #     case 'managers':
    #         bots = await bots.get_manager_bots()
    #     case 'parsers':
    #         bots = await bots.get_parser_bots()
    #     case _:
    #         raise HTTPException(status_code=404, detail='Role not found')
    bots = await bots.get_all_bots()
    campaigns = await campaigns.get_campaigns()
    return templates.TemplateResponse(
        request=request,
        name='bots.html',
        context={
            'bots': bots,
            'campaigns': campaigns,
        }
    )
