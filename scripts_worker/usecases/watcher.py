from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import Annotated, Optional

from httpx import AsyncClient
from pydantic import BaseModel, parse_obj_as

from abstractions.usecases.notificator import NotificatorInterface
from abstractions.usecases.watcher import WatcherInterface
from domain.models import ChatProcess
from domain.reports import SetChatStatusRequest, SetMessageStatusRequest, SetScriptStatusRequest, SetTargetChatsRequest


@dataclass
class Watcher(WatcherInterface):
    notificator: NotificatorInterface

    base_url: str = ''

    new_activation_endpoint: str = ''
    target_chats_endpoint: str = ''
    script_status_endpoint: str = ''
    chat_status_endpoint: str = ''
    message_status_endpoint: str = ''

    processes_to_sfc: dict[
        Annotated[str, 'script process id'],
        Annotated[str, 'active script id']
    ] = field(default_factory=dict)

    @asynccontextmanager
    async def _get_client(self) -> AsyncClient:
        async with AsyncClient(base_url=self.base_url) as client:
            yield client

    async def report_new_activation(self, sfc_id: str) -> Annotated[str, 'Process ID to send further reports']:
        async with self._get_client() as client:  # type: AsyncClient
            response = await client.post(
                url=self.new_activation_endpoint,
                json={
                    'sfc_id': sfc_id,
                },
            )

            response.raise_for_status()

            process_id = response.content.decode()

            self.processes_to_sfc[process_id] = sfc_id

            # print(process_id)
            return process_id

    async def _report(self, report: BaseModel, endpoint: str, fail_silent: bool = True) -> Optional[dict]:
        async with self._get_client() as client:  # type: AsyncClient
            response = await client.post(
                url=endpoint,
                json=report.model_dump(),
            )

            if not fail_silent:
                response.raise_for_status()

            try:
                return response.json()
            except:
                ...

    async def report_target_chats(self, report: SetTargetChatsRequest) -> list[ChatProcess]:
        res = await self._report(
            report=report,
            endpoint=self.target_chats_endpoint,
            fail_silent=False,
        )

        res = parse_obj_as(list[ChatProcess], res)

        await self.notificator.script_started(
            sfc_id=self.processes_to_sfc[report.process_id],
            target_chats=report.target_chats,
        )

        return res

    async def report_script_status(self, report: SetScriptStatusRequest):
        await self._report(
            report=report,
            endpoint=self.script_status_endpoint,
        )

        await self.notificator.script_finished(
            sfc_id=self.processes_to_sfc[report.process_id],
            is_successful=report.is_successful,
        )

    async def report_message_status(self, report: SetMessageStatusRequest):
        await self._report(
            report=report,
            endpoint=self.message_status_endpoint,
        )

    async def report_chat_status(self, report: SetChatStatusRequest):
        await self._report(
            report=report,
            endpoint=self.chat_status_endpoint,
        )

        if not report.is_successful:
            await self.notificator.chat_skipped(
                sfc_id=self.processes_to_sfc[report.process_id],
                chat_link=report.chat_link,
                on_message=report.on_message,
                reason=report.reason,
            )
