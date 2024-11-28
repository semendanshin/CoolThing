from abstractions.services.telegram.notificator import NotificatorInterface
from dependencies.bot import get_bot
from services.telegram import TelegramNotificator


def get_notificator() -> NotificatorInterface:
    return TelegramNotificator(
        bot=get_bot(),
    )
