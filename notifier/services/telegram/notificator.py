import logging
from dataclasses import dataclass

from telegram import Bot

from abstractions.services.telegram.notificator import NotificatorInterface
from domain.notifications import Notification

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class TelegramNotificator(NotificatorInterface):
    bot: Bot

    async def send(self, notification: Notification) -> None:
        await self.bot.send_message(
            chat_id=notification.send_to,
            text=notification.text,
        )
