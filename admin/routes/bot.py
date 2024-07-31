from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from abstractions.usecases.CampaingsUseCaseInterface import CampaignsUseCaseInterface
from dependencies.usecases.campaign import get_campaigns_usecase
from domain.dto.worker import WorkerUpdateDTO
from forms.bot_connect_2fa_form import bot_connect_2fa_form
from forms.bot_connect_form import bot_connect_form
from forms.bot_create_form import bot_create_form
from dependencies.usecases.bots import get_bots_usecase
from domain.schemas.bots import BotCreate, BotConnect, BotConnect2FA, ParserBotDetails, ManagerBotDetails
from abstractions.usecases.BotsUseCaseInterface import BotsUseCaseInterface
from forms.bot_update import update_worker_form

router = APIRouter(
    prefix='/bot',
    tags=['Bot'],
)

templates = Jinja2Templates(directory='templates')


@router.get("/new")
async def get_new_bot(
        request: Request,
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name='new_bot.html',
        context={},
    )


@router.post("")
async def create_new_bot(
        bot: BotCreate = Depends(bot_create_form),
        bots: BotsUseCaseInterface = Depends(get_bots_usecase),
) -> RedirectResponse:
    print(bot.model_dump())
    await bots.create(bot)
    return RedirectResponse(url='/bots', status_code=303)
    # return RedirectResponse(url='/bots/connect', status_code=303)


@router.get("/connect")
async def get_connect_bot(
        request: Request,
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name='connect_bot.html',
        context={},
    )


@router.post("/connect")
async def connect_bot(
        connection: BotConnect = Depends(bot_connect_form),
        bots: BotsUseCaseInterface = Depends(get_bots_usecase),
) -> RedirectResponse:
    print(connection.model_dump())
    if await bots.connect_bot_by_code(connection.auth_code):
        return RedirectResponse(url='/bots', status_code=303)

    return RedirectResponse(url='/bots/connect/2fa', status_code=303)


@router.get("/connect/2fa")
async def get_2fa_bot(
        request: Request,
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name='2fa_bot.html',
        context={},
    )


@router.post("/connect/2fa")
async def connect_2fa_bot(
        bot_connection: BotConnect2FA = Depends(bot_connect_2fa_form),
        bots: BotsUseCaseInterface = Depends(get_bots_usecase),
) -> RedirectResponse:
    if not await bots.connect_bot_by_password(bot_connection.password):
        return RedirectResponse(url='/fallback', status_code=303)

    return RedirectResponse(url='/bots', status_code=303)


@router.get("/{bot_id}")
async def get_bot(
        bot_id: str,
        request: Request,
        bots: BotsUseCaseInterface = Depends(get_bots_usecase),
        campaigns: CampaignsUseCaseInterface = Depends(get_campaigns_usecase),
) -> HTMLResponse:
    bot = await bots.get_bot(bot_id)
    campaigns_list = await campaigns.get_campaigns()

    return templates.TemplateResponse(
        request=request,
        name='bot.html',
        context={
            'bot': bot,
            'campaigns': campaigns_list,
        }
    )


@router.post("/{bot_id}")
async def update_bot_backend(
        bot_id: str,
        update_schema: WorkerUpdateDTO = Depends(update_worker_form),
        bots: BotsUseCaseInterface = Depends(get_bots_usecase),
) -> RedirectResponse:
    await bots.update(bot_id, update_schema)
    return RedirectResponse(url=f'/bot/{bot_id}', status_code=303)
