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
            username: str,
            text: str,
    ) -> None:
        pass
