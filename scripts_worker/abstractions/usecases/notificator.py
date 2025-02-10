from abc import ABC, abstractmethod


class NotificatorInterface(ABC):
    @abstractmethod
    async def script_started(self, sfc_id: str, target_chats: list[str]) -> None:
        ...

    @abstractmethod
    async def script_finished(self, sfc_id: str, is_successful: bool, problems: list[str] = None) -> None:
        ...

    @abstractmethod
    async def chat_skipped(self, sfc_id: str, chat_link: str, on_message: str = None, reason: str = None) -> None:
        ...
