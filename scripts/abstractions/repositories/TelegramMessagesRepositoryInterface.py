from abc import ABC, abstractmethod

from domain.models import Worker


class TelegramMessagesRepositoryInterface(
    ABC,
):
    @abstractmethod
    async def send_message(
            self,
            app_id: str,
            app_hash: str,
            session_string: str,
            chat_id: str,
            text: str,
            reply_to: int,
    ) -> int:
        pass

    @abstractmethod
    async def join_chat(self, worker: Worker, chat: str | int):
        ...

