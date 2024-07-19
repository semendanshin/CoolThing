from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from abstractions.AbstractChatsService import AbstractChatsService
from dependencies.bots_service import get_bots_service
from abstractions.AbstractBotsService import AbstractBotsService
from dependencies.chat_service import get_chats_service

router = APIRouter(
    prefix='/chats',
    tags=['Chats'],
)

templates = Jinja2Templates(directory='templates')

@router.get("")
async def get_all_chats(
        request: Request,
        chats_service: AbstractChatsService = Depends(get_chats_service),
) -> HTMLResponse:
    chats = await chats_service.get_all_chats()
    return templates.TemplateResponse(
        request=request,
        name='chats.html',
        context={
            'chat_items': chats,
            'chat': None,
        }
    )

@router.get("/{chat_id}")
async def get_one_chat(
        chat_id: str,
        request: Request,
        chats_service: AbstractChatsService = Depends(get_chats_service),
) -> HTMLResponse:
    chats = await chats_service.get_all_chats()
    main_chat = await chats_service.get_chat(chat_id=chat_id)
    return templates.TemplateResponse(
        request=request,
        name='chats.html',
        context={
            'chat_items': chats,
            'chat': main_chat,
        }
    )
