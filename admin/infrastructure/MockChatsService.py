from typing import Optional

from abstractions.AbstractChatsService import AbstractChatsService
from domain.chats import Chat, ChatInfo, Message


class MockChatsService(AbstractChatsService):
    async def get_all_chats(self, page: int = 0, size: int = 10) -> list[Optional[ChatInfo]]:
        return [
            ChatInfo(
                chat_id="1",
                bot_nickname="bot",
                user_nickname="user",
                user_id="1",
                last_message="Hello",
                status="online",
            ),
            ChatInfo(
                chat_id="2",
                bot_nickname="bot",
                user_nickname="user",
                user_id="2",
                last_message="Hello",
                status="offline",
            ),
        ]

    async def get_chat(self, chat_id: str) -> Optional[Chat]:
        return Chat(
            info=ChatInfo(
                chat_id="1",
                bot_nickname="bot",
                user_nickname="user",
                user_id="1",
                last_message="Hello",
                status="online",
            ),
            messages=[
                Message(
                    text="Hello",
                    sent_at="2021-01-01T00:00:00",
                    type="outcome",
                ),
                Message(
                    text="Hello",
                    sent_at="2021-01-01T00:01:00",
                    type="income",
                ),
                Message(
                    text="How are you?",
                    sent_at="2021-01-01T00:02:00",
                    type="outcome",
                ),
            ],
        )

