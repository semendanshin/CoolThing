from abc import ABC, abstractmethod

from domain.models.script import ChatProcess


class ActiveScriptProcessServiceInterface(ABC):
    @abstractmethod
    async def new_activation_received(self, sfc_id: str) -> str:
        ...

    @abstractmethod
    async def set_target_chats(self, process_id: str, target_chats: list[str]) -> list[ChatProcess]:
        ...

    @abstractmethod
    async def set_script_status(self, process_id: str, is_successful: bool, is_processed: bool):
        ...

    @abstractmethod
    async def set_message_status(self, process_id: str, message_id: str, send: bool, text: str = None):
        ...

    @abstractmethod
    async def set_chat_status(self, process_id: str, chat_link: str, is_processed: bool, is_successful: bool):
        ...
