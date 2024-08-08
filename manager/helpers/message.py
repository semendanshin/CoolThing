import asyncio
from dataclasses import dataclass
from random import randint
from typing import Annotated

from pyrogram import Client
from pyrogram.enums import ChatAction

from abstractions.helpers.message import MessageHelperInterface


@dataclass
class SendingMessageHelper(MessageHelperInterface):
    app: Client

    async def set_typing_status(
            self,
            chat_id: int,
    ) -> None:
        await self.app.send_chat_action(chat_id, ChatAction.TYPING)

    async def send_message(
            self,
            chat_id: int,
            text: str,
    ) -> None:
        await self.app.send_message(chat_id, text)
