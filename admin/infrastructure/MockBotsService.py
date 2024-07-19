from domain.bots import ManagerBotOverview, ParserBotOverview, ManagerBotDetails, ParserBotDetails
from abstractions.AbstractBotsService import AbstractBotsService


class MockBotsService(AbstractBotsService):
    parsers = False

    async def get_manager_bots(self) -> list[ManagerBotOverview]:
        return [
            ManagerBotOverview(
                nickname="@nedvigadlyacseh",
                scope="estate",
                messages_count=150,
                chats_ratio="15/30",
                proxy="0.0.0.0",
                proxy_status=True,
                unread_messages=10,
            ),
            ManagerBotOverview(
                nickname="@adsforyou",
                scope="advertisement",
                messages_count=150,
                chats_ratio="15/30",
                proxy="0.0.0.0",
                proxy_status=False,
                unread_messages=10,
            ),
            ManagerBotOverview(
                nickname="@ManagerAlfabank",
                scope="money",
                messages_count=150,
                chats_ratio="15/30",
                proxy="0.0.0.0",
                proxy_status=True,
                unread_messages=10,
            ),
        ]

    async def get_parser_bots(self) -> list[ParserBotOverview]:
        return [
            ParserBotOverview(
                nickname="@nedvigadlyacseh",
                scope="estate",
                positive_keywords=["positive", "good"],
                negative_keywords=["negative", "bad"],
                chats=["chat1", "chat2"],
                proxy="0.0.0.0",
                proxy_status=True,
            ),
            ParserBotOverview(
                nickname="@adsforyou",
                scope="advertisement",
                positive_keywords=["positive", "good"],
                negative_keywords=["negative", "bad"],
                chats=["chat1", "chat2"],
                proxy="0.0.0.0",
                proxy_status=False,
            ),
            ParserBotOverview(
                nickname="@ManagerAlfabank",
                scope="money",
                positive_keywords=["positive", "good"],
                negative_keywords=["negative", "bad"],
                chats=["chat1", "chat2"],
                proxy="0.0.0.0",
                proxy_status=True,
            ),
        ]

    async def connect_bot_by_code(self, code: str) -> bool:
        return False

    async def connect_bot_by_password(self, password: str) -> bool:
        return False

    async def get_bot(self, bot_username: str) -> ManagerBotDetails | ParserBotDetails:
        if self.parsers:
            return ParserBotDetails(
                nickname="@adsforyou",
                bio="I am a bot for ads",
                scope="advertisement",
                positive_keywords=["positive", "good"],
                negative_keywords=["negative", "bad"],
                chats=["chat1", "chat2"],
                proxy="0.0.0.0",
                avatar="https://example.com/avatar.jpg",
            )

        return ManagerBotDetails(
            nickname="@ManagerAlfabank",
            bio="I am a bot for money",
            scope="money",
            chats=10,
            proxy="0.0.0.0",
            api_key="api_key",
            chatgpt_model="chatgpt_model",
            chatgpt_assistant="chatgpt_assistant",
            avatar="https://example.com/avatar.jpg",
        )
