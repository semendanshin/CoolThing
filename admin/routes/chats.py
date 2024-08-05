from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from abstractions.usecases import BotsUseCaseInterface
from abstractions.usecases.CampaingsUseCaseInterface import CampaignsUseCaseInterface
from abstractions.usecases.ChatsUseCaseInterface import ChatsUseCaseInterface
from abstractions.usecases.MessagesUseCaseInterface import MessagesUseCaseInterface
from dependencies.usecases.bots import get_bots_usecase
from dependencies.usecases.campaign import get_campaigns_usecase
from dependencies.usecases.chats import get_chats_service
from dependencies.usecases.messages import get_messages_service
from domain.dto.chat import UpdateAutoReplyDTO, SendMessageDTO
from forms.auto_reply_update_from import auto_reply_update_form
from forms.send_message_form import send_message_form

router = APIRouter(
    prefix='/chats',
    tags=['Chats'],
)

templates = Jinja2Templates(directory='templates')


@router.get("")
async def get_all_chats(
        request: Request,
        chats_service: ChatsUseCaseInterface = Depends(get_chats_service),
        bots_service: BotsUseCaseInterface = Depends(get_bots_usecase),
        campaigns_usecase: CampaignsUseCaseInterface = Depends(get_campaigns_usecase),
) -> HTMLResponse:
    chats = await chats_service.get_all_chats()
    bots = [await bots_service.get_by_username(chat.bot_nickname) for chat in chats]
    campaigns = await campaigns_usecase.get_campaigns()
    print(chats)
    return templates.TemplateResponse(
        request=request,
        name='chats.html',
        context={
            'chat_items': chats,
            'chat': None,
            'bots': bots,
            'campaigns': campaigns,
        }
    )


@router.get("/{chat_id}")
async def get_one_chat(
        chat_id: str,
        request: Request,
        chats_service: ChatsUseCaseInterface = Depends(get_chats_service),
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


@router.post("/{chat_id}/send")
async def send_message_backend(
        chat_id: str,
        message: SendMessageDTO = Depends(send_message_form),
        messages_service: MessagesUseCaseInterface = Depends(get_messages_service),
) -> RedirectResponse:
    await messages_service.send_and_save_message(
        chat_id=chat_id, text=message.message
    )
    return RedirectResponse(url=f"/chats/{chat_id}", status_code=303)


@router.post("/{chat_id}/auto_reply")
async def auto_reply_backend(
        chat_id: str,
        from_schema: UpdateAutoReplyDTO = Depends(auto_reply_update_form),
        chats_service: ChatsUseCaseInterface = Depends(get_chats_service),
) -> RedirectResponse:
    await chats_service.set_auto_reply(chat_id=chat_id, auto_reply=from_schema.auto_reply)
    return RedirectResponse(url=f"/chats/{chat_id}", status_code=303)
