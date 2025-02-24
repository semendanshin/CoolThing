from dataclasses import dataclass
from typing import Optional

from pydantic import SecretStr
from telegram import Bot
from telegram.ext import Application, CommandHandler

from bot.handlers import start_command


@dataclass
class BotProvider:
    token: SecretStr
    _bot: Optional[Bot] = None

    def __post_init__(self):
        self.setup_bot()

    @property
    def bot(self):
        return self._bot

    @bot.setter
    def bot(self, value):
        raise Exception("You can't set a value for this field")

    def setup_bot(self):
        if not self._bot:
            self._bot = Bot(token=self.token.get_secret_value())

    def setup_application(self) -> Application:
        app = Application.builder().bot(self.bot).build()

        app.add_handler(CommandHandler('start', start_command))
        return app
