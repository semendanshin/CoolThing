from abc import ABC, abstractmethod

from abstractions.repositories import CRUDRepositoryInterface
from domain.dto.script import ActiveScriptProcessCreateDTO, ActiveScriptProcessUpdateDTO
from domain.models.script import ActiveScriptProcess, ChatProcess


class ActiveScriptProcessRepositoryInterface(
    CRUDRepositoryInterface[
        ActiveScriptProcess, ActiveScriptProcessCreateDTO, ActiveScriptProcessUpdateDTO,
    ],
    ABC,
):
    @abstractmethod
    async def set_target_chats(self, process_id: str, target_chats: list[str]):
        ...

    @abstractmethod
    async def end_script(self, process_id: str, is_successful: bool, is_processed: bool):
        ...

    @abstractmethod
    async def end_chat(self, process_id: str, chat_link: str, is_successful: bool, is_processed: bool):
        ...

    @abstractmethod
    async def end_message(self, process_id: str, message_id: str, send: bool, text: str):
        ...

    @abstractmethod
    async def set_process(self, process_id: str, process: list[ChatProcess]):
        ...
