from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from dependencies.bots_service import get_bots_service
from abstractions.AbstractBotsService import AbstractBotsService

router = APIRouter(
    prefix='/bots',
    tags=['Bots'],
)

templates = Jinja2Templates(directory='templates')


@router.get("")
async def get_all_bots() -> RedirectResponse:
    return RedirectResponse(url='/bots/managers')


@router.get("/managers")
async def get_manager_bots(
        request: Request,
        bots: AbstractBotsService = Depends(get_bots_service),
) -> HTMLResponse:
    bots_overview = await bots.get_manager_bots()
    return templates.TemplateResponse(
        request=request,
        name='manager_bots.html',
        context={
            'bots': bots_overview,
            'active': 'managers',
        }
    )


@router.get("/parsers")
async def get_manager_bots(
        request: Request,
        bots: AbstractBotsService = Depends(get_bots_service),
) -> HTMLResponse:
    bots_overview = await bots.get_parser_bots()
    return templates.TemplateResponse(
        request=request,
        name='parser_bots.html',
        context={
            'bots': bots_overview,
            'active': 'parsers',
        }
    )
