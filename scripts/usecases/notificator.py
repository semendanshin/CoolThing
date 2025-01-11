from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime

from httpx import AsyncClient

from abstractions.usecases.notificator import NotificatorInterface
from domain.reports.notifier import Service, ScriptStartedNotification, Notification, ScriptFinishedNotification, \
    ChatSkippedNotification


@dataclass
class Notificator(NotificatorInterface):
    service: Service

    base_url: str

    events_endpoint: str = '/events'

    @asynccontextmanager
    async def _get_client(self):
        async with AsyncClient(base_url=self.base_url) as client:
            yield client

    async def notify(self, notification: Notification) -> None:
        async with self._get_client() as client:
            await client.post(
                url=self.events_endpoint,
                json=notification.model_dump_json(),
            )

    async def script_started(self, sfc_id: str, target_chats: list[str]) -> None:
        report = ScriptStartedNotification(
            sfc_id=sfc_id,
            chats=target_chats,
            service=self.service,
        )

        await self.notify(report)

    async def script_finished(self, sfc_id: str, is_successful: bool, problems: list[str] = None) -> None:
        report = ScriptFinishedNotification(
            sfc_id=sfc_id,
            finished_at=datetime.now(),
            problems=problems if problems else [],
            service=self.service,
        )

        await self.notify(report)

    async def chat_skipped(self, sfc_id: str, chat_link: str, on_message: str = None, reason: str = None) -> None:
        report = ChatSkippedNotification(
            sfc_id=sfc_id,
            chat_link=chat_link,
            on_message=on_message,
            reason=reason,
            service=self.service,
        )

        await self.notify(report)
