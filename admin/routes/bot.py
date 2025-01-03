from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from abstractions.usecases.BotsUseCaseInterface import BotsUseCaseInterface
from abstractions.usecases.CampaingsUseCaseInterface import CampaignsUseCaseInterface
from dependencies.usecases.bots import get_bots_usecase
from dependencies.usecases.campaign import get_campaigns_usecase
from domain.dto.worker import WorkerUpdateDTO, WorkerCreateDTO
from domain.schemas.bots import BotConnect, BotConnect2FA, BotCreateBase
from forms.bot_connect_2fa_form import bot_connect_2fa_form
from forms.bot_connect_form import bot_connect_form
from forms.bot_create_form import bot_create_form
from forms.bot_create_full_form import bot_create_full_form
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
async def create_new_bot_backend(
        bot: BotCreateBase = Depends(bot_create_form),
        bots: BotsUseCaseInterface = Depends(get_bots_usecase),
) -> RedirectResponse:
    await bots.send_code(bot.app_id, bot.app_hash, bot.phone, bot.proxy)
    return RedirectResponse(
        url=f'/bot/connect?app_id={bot.app_id}&phone={bot.phone}&'
            f'app_hash={bot.app_hash}&proxy={bot.proxy if bot.proxy else ""}',
        status_code=303)


@router.get("/connect")
async def get_connect_bot(
        app_id: int,
        app_hash: str,
        phone: str,
        request: Request,
        proxy: Optional[str] = None,
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name='connect_bot.html',
        context={
            'app_id': app_id,
            'app_hash': app_hash,
            'phone': phone,
            'proxy': proxy,
        },
    )


@router.post("/connect")
async def connect_bot_backend(
        connection: BotConnect = Depends(bot_connect_form),
        bots: BotsUseCaseInterface = Depends(get_bots_usecase),
) -> RedirectResponse:
    if session_string := await bots.authorize(connection.app_id, connection.auth_code):
        print(f"no 2fa needed, {connection.proxy}, {type(connection.proxy)}")
        url = f'/bot/new/finalize?app_id={connection.app_id}&' \
              f'phone={connection.phone}&' \
              f'app_hash={connection.app_hash}&' \
              f'session_string={session_string}&' \
              f'proxy={connection.proxy if connection.proxy else ""}'
        print(url)
        return RedirectResponse(
            url=url,
            status_code=303
        )
    return RedirectResponse(
        url=f'/bot/connect/2fa?app_id={connection.app_id}&'
            f'phone={connection.phone}&'
            f'app_hash={connection.app_hash}&'
            f'proxy={connection.proxy}',
        status_code=303
    )


@router.get("/connect/2fa")
async def get_2fa_bot(
        app_id: int,
        app_hash: str,
        phone: str,
        request: Request,
        proxy: Optional[str] = None,
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name='2fa_bot.html',
        context={
            'app_id': app_id,
            'app_hash': app_hash,
            'phone': phone,
            'proxy': proxy,
        },
    )


@router.post("/connect/2fa")
async def connect_2fa_bot(
        bot_connection: BotConnect2FA = Depends(bot_connect_2fa_form),
        bots: BotsUseCaseInterface = Depends(get_bots_usecase),
) -> RedirectResponse:
    if not (session_string := await bots.authorize_2fa(bot_connection.app_id, bot_connection.password)):
        return RedirectResponse(url='/fallback', status_code=303)
    return RedirectResponse(
        url=f'/bot/new/finalize?app_id={bot_connection.app_id}&'
            f'phone={bot_connection.phone}&'
            f'app_hash={bot_connection.app_hash}&'
            f'session_string={session_string}&'
            f'proxy={bot_connection.proxy}',
        status_code=303
    )


@router.get("/new/finalize")
async def get_finalize_bot(
        app_id: int,
        app_hash: str,
        phone: str,
        session_string: str,
        request: Request,
        campaigns: CampaignsUseCaseInterface = Depends(get_campaigns_usecase),
        proxy: Optional[str] = None,
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name='finalize_bot.html',
        context={
            'bot': {
                'app_id': app_id,
                'app_hash': app_hash,
                'phone': phone,
                'session_string': session_string,
                'proxy': proxy,
            },
            'campaigns': await campaigns.get_campaigns(),
        },
    )


@router.post("/new/finalize")
async def finalize_bot_backend(
        bot: WorkerCreateDTO = Depends(bot_create_full_form),
        bots: BotsUseCaseInterface = Depends(get_bots_usecase),
) -> RedirectResponse:
    await bots.create(bot)
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
            'delete_url': f"/bot/{bot.id}",
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


@router.delete("/{bot_id}")
async def delete_bot_backend(
        bot_id: str,
        bots: BotsUseCaseInterface = Depends(get_bots_usecase),
) -> RedirectResponse:
    await bots.delete(bot_id)
    return RedirectResponse(url='/bots', status_code=303)
