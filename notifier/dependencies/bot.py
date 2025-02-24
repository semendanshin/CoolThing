from telegram import Bot
from telegram.ext import Application

from bot import BotProvider
from settings import settings

bot_provider = BotProvider(token=settings.bot.token)


def get_bot() -> Bot:
    return bot_provider.bot


def setup_application() -> Application:
    return bot_provider.setup_application()
