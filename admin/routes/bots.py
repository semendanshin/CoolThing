from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException

from dependencies.usecases.bots import get_bots_usecase
from abstractions.usecases.BotsUseCaseInterface import BotsUseCaseInterface

router = APIRouter(
    prefix='/bots',
    tags=['Bots'],
)

templates = Jinja2Templates(directory='templates')


@router.get("")
async def get_all_bots() -> RedirectResponse:
    return RedirectResponse(url='/bots/managers')


@router.get("/{role}")
async def get_manager_bots(
        role: str,
        request: Request,
        bots: BotsUseCaseInterface = Depends(get_bots_usecase),
) -> HTMLResponse:
    match role:
        case 'managers':
            bots = await bots.get_manager_bots()
        case 'parsers':
            bots = await bots.get_parser_bots()
        case _:
            raise HTTPException(status_code=404, detail='Role not found')
    return templates.TemplateResponse(
        request=request,
        name='bots.html',
        context={
            'bots': bots,
            'active': role,
        }
    )
