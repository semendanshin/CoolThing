from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from abstractions.usecases.BotsUseCaseInterface import BotsUseCaseInterface
from abstractions.usecases.CampaingsUseCaseInterface import CampaignsUseCaseInterface
from dependencies.usecases.bots import get_bots_usecase
from dependencies.usecases.campaign import get_campaigns_usecase
from .common import templates

router = APIRouter(
    prefix='/bots',
    tags=['Bots'],
)


@router.get("")
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


@router.get("/entities")
async def get_bots_entities(
        bots_usecase: BotsUseCaseInterface = Depends(get_bots_usecase),
) -> list[dict[str, Any]]:
    usernames = [
        {
            "username": x.username if x.username else "",
            "chats": x.chats if x.chats else [],
        } for x in await bots_usecase.get_available_bots()]
    print(usernames)
    return usernames
