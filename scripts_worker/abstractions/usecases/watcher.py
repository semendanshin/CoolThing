from abc import ABC, abstractmethod
from typing import Annotated

from domain.models import ChatProcess
from domain.reports import SetTargetChatsRequest, SetScriptStatusRequest, SetMessageStatusRequest, SetChatStatusRequest


class WatcherInterface(ABC):
    @abstractmethod
    async def report_new_activation(self, sfc_id: str) -> Annotated[str, 'Process ID to send further reports']:
        ...

    @abstractmethod
    async def report_target_chats(self, report: SetTargetChatsRequest) -> list[ChatProcess]:
        ...

    @abstractmethod
    async def report_script_status(self, report: SetScriptStatusRequest):
        ...

    @abstractmethod
    async def report_message_status(self, report: SetMessageStatusRequest):
        ...

    @abstractmethod
    async def report_chat_status(self, report: SetChatStatusRequest):
        ...
