import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Annotated, Optional
from uuid import uuid4

from apscheduler.schedulers.base import BaseScheduler
from pydantic import BaseModel

from abstractions.repositories.active_script_process import ActiveScriptProcessRepositoryInterface
from abstractions.repositories.script import ScriptsRepositoryInterface
from abstractions.repositories.script_for_campaign import ScriptsForCampaignRepositoryInterface
from abstractions.service.active_script_process import ActiveScriptProcessServiceInterface
from abstractions.service.campaign import CampaignServiceInterface
from domain.dto.script import ActiveScriptProcessCreateDTO
from domain.models.script import ChatProcess, MessageProcess

logger = logging.getLogger(__name__)


class ProcessStatus(BaseModel):
    last_activity: datetime
    max_delay: Optional[int] = None

    disabled: Optional[bool] = None


@dataclass(kw_only=True)
class ActiveScriptProcessService(
    ActiveScriptProcessServiceInterface,
):
    process_repository: ActiveScriptProcessRepositoryInterface
    campaign_service: CampaignServiceInterface
    script_repository: ScriptsRepositoryInterface
    sfc_repository: ScriptsForCampaignRepositoryInterface

    scheduler: BaseScheduler

    decision_delay: Annotated[int, 'Threshold of marking script failed if inactive']

    active_processes: dict[
        Annotated[str, 'Process ID'],
        ProcessStatus,
    ] = field(default_factory=dict)

    disabled_processes: list[
        Annotated[str, 'IDs of processed/failed processes'],
    ] = field(default_factory=list)

    def __post_init__(self):
        self.scheduler.start()

    async def new_activation_received(self, sfc_id: str) -> str:
        dto = ActiveScriptProcessCreateDTO(
            sfc_id=sfc_id,
        )

        await self.process_repository.create(
            obj=dto,
        )

        process_id = str(dto.id)

        self.active_processes[process_id] = ProcessStatus(
            last_activity=datetime.now(),
            max_delay=6000,
        )

        return process_id

    def _get_fail_time(self, process_delay: int) -> int:
        return process_delay + self.decision_delay

    def _set_up_check(self, process_id: str):
        process_delay = self.active_processes[process_id].max_delay
        self.scheduler.add_job(
            self._check_process,
            args=(process_id,),
            next_run_time=datetime.now() + timedelta(seconds=self._get_fail_time(process_delay)),
            max_instances=1,
        )

    async def _check_process(self, process_id: str):
        if process_id not in self.active_processes:
            logger.info(f"Process {process_id} is already ended, no actions needed")
            return

        process = self.active_processes[process_id]

        logger.info(f"greatest possible delay for process {process_id} is {process.max_delay + self.decision_delay}")
        if (process.last_activity + timedelta(
                seconds=process.max_delay + self.decision_delay
        ) < datetime.now()):
            await self.set_script_status(
                process_id=process_id,
                is_successful=False,
                is_processed=False,
            )
            del self.active_processes[process_id]
            logger.info(f'Process {process_id} was inactive and considered failed')
        else:
            if process.disabled:
                logger.info(f"Process {process_id} is already ended, no actions needed")
                return

            logger.info(f'Process {process_id} was active since last check, setting up new check')
            self._set_up_check(process_id)

    async def set_target_chats(self, process_id: str, target_chats: list[str]) -> list[ChatProcess]:
        await self.process_repository.set_target_chats(process_id, target_chats)

        process = await self.process_repository.get(process_id)

        sfc = await self.sfc_repository.get(process.sfc_id)
        script = await self.script_repository.get(sfc.script_id)

        process = []

        for chat in target_chats:
            current = ChatProcess(
                chat_link=chat,
                messages=[],
            )

            messages = []
            for message in script.messages:
                message_process = MessageProcess(
                    id=str(uuid4()),
                    text=message.text,
                    bot_id=sfc.bots_mapping[str(message.bot_index)],
                )
                messages.append(message_process)

            current.messages = messages
            process.append(current)

        await self.process_repository.set_process(
            process_id=process_id,
            process=process,
        )

        campaign_id = sfc.campaign_id
        delay = await self.campaign_service.get_maximum_campaign_delay(campaign_id)

        self.active_processes[process_id] = ProcessStatus(
            last_activity=datetime.now(),
            max_delay=delay,
        )

        self._set_up_check(process_id)

        return process

    async def set_script_status(self, process_id: str, is_successful: bool, is_processed: bool):
        await self.process_repository.end_script(
            process_id=process_id,
            is_successful=is_successful,
            is_processed=is_processed
        )

        if not is_processed:  # actually is "if not is_successful and not is_processed"
            process = await self.process_repository.get(process_id)
            for chat in process.process:
                await self.process_repository.end_chat(
                    process_id=process_id,
                    chat_link=chat.chat_link,
                    is_successful=False,
                    is_processed=False,
                )
            return

        self.disable_process(process_id)

    def update_activity(self, process_id: str):
        self.active_processes[process_id].last_activity = datetime.now()

    def disable_process(self, process_id: str):
        self.update_activity(process_id)
        self.active_processes[process_id].disabled = True

    async def set_message_status(self, process_id: str, message_id: str, send: bool, text: str = None):
        await self.process_repository.end_message(
            process_id=process_id,
            message_id=message_id,
            send=send,
            text=text,
        )

        self.update_activity(process_id)
        # self._set_up_check(process_id)

    async def set_chat_status(
            self,
            process_id: str,
            chat_link: str,
            is_processed: bool,
            is_successful: bool,
    ):
        await self.process_repository.end_chat(
            process_id=process_id,
            chat_link=chat_link,
            is_successful=is_successful,
            is_processed=is_processed,
        )

        self.update_activity(process_id)
