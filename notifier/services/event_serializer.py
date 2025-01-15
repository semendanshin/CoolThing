import time
from dataclasses import dataclass
from datetime import datetime

from abstractions.repositories.ScriptsForCampaignRepositoryInterface import ScriptsForCampaignRepositoryInterface
from abstractions.services.bots import BotsServiceInterface
from abstractions.services.event_serializer import EventSerializerInterface
from domain.events import EventType, EventTypes


@dataclass
class EventSerializer(EventSerializerInterface):
    workers: BotsServiceInterface
    active_scripts: ScriptsForCampaignRepositoryInterface

    async def get_event_string(self, event: EventTypes) -> str:
        time_format = "%H:%M:%S %d.%m.%Y"

        def strftime(dt: datetime) -> str:
            return dt.time().strftime(time_format)

        match event.type:
            case EventType.BOT_BANNED:
                bot = await self.workers.get_bot(event.worker_id)
                message = f'Бот {bot.username} забанен в {strftime(event.created_at)}, комментарий: {event.comment}'

            case EventType.CHAT_SKIPPED:
                active_script = await self.active_scripts.get(str(event.sfc_id))  # TODO: bad, need consistent types
                message = f'Чат {event.chat_id} пропущен во время выполнения сценария {active_script.script_id}, ' \
                          f'запущенного в {strftime(active_script.created_at)}. ' \
                          f'Сообщение: {event.on_message}\nПричина: {event.reason}'

            case EventType.SCRIPT_CRASHED:
                active_script = await self.active_scripts.get(str(event.sfc_id))  # TODO: bad, need consistent types
                message = f'Сценарий {active_script.script_id}, запущенный в {strftime(active_script.created_at)} упал в чате {event.chat_id}. ' \
                          f'Сообщение: {event.on_message}\nПричина: {event.reason}'

            case EventType.SERVICE_CRASHED:
                message = f'**КРИТИЧЕСКАЯ ОШИБКА**\n\nСервис {event.service.name} аварийно остановлен в {strftime(event.created_at)}.' \
                          f'\nПричина: {event.reason}'

            case EventType.SCRIPT_STARTED:
                active_script = await self.active_scripts.get(str(event.sfc_id))  # TODO: bad, need consistent types
                message = f'Запущен сценарий {active_script.script_id} в {strftime(active_script.created_at)}.\n\nЧаты: {"\n".join(map(str, event.chats))}'

            case EventType.SCRIPT_FINISHED:
                finished_script = await self.active_scripts.get(str(event.sfc_id))
                message = f'Сценарий {finished_script.script_id} закончил работу в {strftime(event.finished_at)}.\n\n'

                if event.problems:
                    problems = 'Проблемы:\n' + '\n'.join(map(str, event.problems))
                else:
                    problems = 'Во время выполнения сценария не возникло проблем'
                message += problems

            case _:
                return f'Неизвестное событие произошло в сервисе {event.created_by.name} в {event.created_at}. ' \
                       f'Полученный тип события - {event.type}'

        return message
