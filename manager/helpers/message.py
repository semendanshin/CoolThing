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
            delay_from: Annotated[int, "seconds"],
            delay_to: Annotated[int, "seconds"],
    ) -> None:
        await asyncio.sleep(randint(delay_from, delay_to))
        await self.app.send_chat_action(chat_id, ChatAction.TYPING)

    async def send_message(
            self,
            chat_id: int,
            text: str,
            delay_from: Annotated[int, "seconds"],
            delay_to: Annotated[int, "seconds"],
    ) -> None:
        await asyncio.sleep(randint(delay_from, delay_to))
        await self.app.send_message(chat_id, text)
