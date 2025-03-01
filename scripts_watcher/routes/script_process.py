import logging
from typing import Annotated

from fastapi import APIRouter

from dependencies.services.active_script_process import get_active_script_process_service
from domain.models.script import ChatProcess
from domain.requests import (
    NewActivationRequest,
    SetTargetChatsRequest,
    SetScriptStatusRequest,
    SetMessageStatusRequest,
    SetChatStatusRequest
)

router = APIRouter(
    prefix='/scripts-process',
    tags=['Script process state'],
)

logger = logging.getLogger(__name__)


@router.post('/received')
async def activation_received(
        req: NewActivationRequest,
) -> Annotated[str, 'Process ID']:
    service = get_active_script_process_service()

    logger.info(req.model_dump())
    process_id = await service.new_activation_received(
        sfc_id=req.sfc_id,
    )

    return process_id


@router.post('/target-chats')
async def set_target_chats(
        req: SetTargetChatsRequest,
) -> list[ChatProcess]:
    service = get_active_script_process_service()

    logger.info(req.model_dump())

    req.process_id = req.process_id.strip('"')

    logger.info(req.model_dump())

    process = await service.set_target_chats(
        process_id=req.process_id,
        target_chats=req.target_chats,
    )

    return process


@router.post('/script')
async def set_script_status(
        req: SetScriptStatusRequest,
) -> None:
    service = get_active_script_process_service()

    req.process_id = req.process_id.strip('"')

    await service.set_script_status(
        process_id=req.process_id,
        is_successful=req.is_successful,
        is_processed=True,
    )


@router.post('/message')
async def set_message_status(
        req: SetMessageStatusRequest,
) -> None:
    service = get_active_script_process_service()

    req.process_id = req.process_id.strip('"')

    await service.set_message_status(
        process_id=req.process_id,
        message_id=req.message_id,
        send=req.is_sent,
        text=req.text,
    )


@router.post('/chat')
async def set_chat_status(
        req: SetChatStatusRequest,
) -> None:
    service = get_active_script_process_service()

    req.process_id = req.process_id.strip('"')

    await service.set_chat_status(
        process_id=req.process_id,
        chat_link=req.chat_link,
        is_successful=req.is_successful,
        is_processed=True,
    )
