from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Annotated

from httpx import AsyncClient
from pydantic import BaseModel, parse_obj_as

from abstractions.usecases.watcher import WatcherInterface
from domain.models import ChatProcess
from domain.reports import SetChatStatusRequest, SetMessageStatusRequest, SetScriptStatusRequest, SetTargetChatsRequest


@dataclass
class Watcher(WatcherInterface):
    base_url: str = ''

    new_activation_endpoint: str = ''
    target_chats_endpoint: str = ''
    script_status_endpoint: str = ''
    chat_status_endpoint: str = ''
    message_status_endpoint: str = ''

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

            print(process_id)
            return process_id

    async def _report(self, report: BaseModel, endpoint: str) -> dict:
        async with self._get_client() as client:  # type: AsyncClient
            response = await client.post(
                url=endpoint,
                json=report.model_dump(),
            )

            response.raise_for_status()

            return response.json()

    async def report_target_chats(self, report: SetTargetChatsRequest) -> list[ChatProcess]:
        res = await self._report(
            report=report,
            endpoint=self.target_chats_endpoint,
        )

        res = parse_obj_as(list[ChatProcess], res)

        return res

    async def report_script_status(self, report: SetScriptStatusRequest):
        await self._report(
            report=report,
            endpoint=self.script_status_endpoint,
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
