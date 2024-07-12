from domain.bots import BotOverview
from .abstractions.AbstractBotsService import AbstractBotsService


class BotsService(AbstractBotsService):
    async def get_bots(self):
        return [
            BotOverview(
                nickname="@ManagerAlfabank",
                scope="money",
                messages_count=10,
                chats_ratio="7/30",
                proxy="0.0.0.0",
                proxy_status=True,
                unread_messages=0,
            ),
            BotOverview(
                nickname="@nedvigadlyacseh",
                scope="estate",
                messages_count=150,
                chats_ratio="15/30",
                proxy="0.0.0.0",
                proxy_status=True,
                unread_messages=0,
            ),
            BotOverview(
                nickname="@adsforyou",
                scope="advertisement",
                messages_count=20,
                chats_ratio="14/50",
                proxy="0.0.0.0",
                proxy_status=False,
                unread_messages=10,
            ),
        ]

    async def connect_bot_by_code(self, code: str) -> bool:
        return False

    async def connect_bot_by_password(self, password: str) -> bool:
        return False
