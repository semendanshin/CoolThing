from abc import ABC, abstractmethod


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
