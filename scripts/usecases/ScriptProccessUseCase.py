import json
import logging
from asyncio import sleep
from dataclasses import dataclass
from random import randint
from typing import AsyncIterable

from aio_pika import IncomingMessage

from abstractions.usecases.WorkersUseCaseInterface import WorkersUseCaseInterface
from abstractions.usecases.CampaignsUseCaseInterface import CampaignsUseCaseInterface
from abstractions.usecases.ScriptsUseCaseInterface import ScriptsUseCaseInterface
from domain.events.scripts import NewActiveScript
from domain.models import ScriptForCampaign as ScriptForCampaignModel
from usecases.exceptions import NoSuchCampaignError, NoSuchScriptError

logger = logging.getLogger(__name__)


@dataclass
class ScriptProcessUseCase:
    scripts_use_case: ScriptsUseCaseInterface
    workers_use_case: WorkersUseCaseInterface
    campaign_use_case: CampaignsUseCaseInterface

    typing_and_sending_sleep_from: int
    typing_and_sending_sleep_to: int

    async def activate_new_script(self, message: IncomingMessage):
        event = NewActiveScript(**json.loads(message.body.decode()))
        logger.info(f"New script activating request received: {event}")

        sfc = await self.scripts_use_case.get_active_script(sfc_id=event.script_for_campaign_id)

        return await self.process_script(sfc)

    async def _get_target_chats(self, sfc: ScriptForCampaignModel) -> list[str]:  # TODO: Annotated
        campaign = await self.campaign_use_case.get_campaign(campaign_id=sfc.campaign_id)
        return campaign.chats

    async def process_script(self, sfc: ScriptForCampaignModel):
        script_id, campaign_id = sfc.script_id, sfc.campaign_id  # TODO: refactor?

        campaign = await self.campaign_use_case.get_campaign(campaign_id)
        if not campaign:
            raise NoSuchCampaignError(f'There is no campaign with id "{campaign_id}"')

        script = await self.scripts_use_case.get_script(script_id)
        if not script:
            raise NoSuchScriptError(f'There is no script with id "{script_id}"')

        target_chats = await self._get_target_chats(sfc)

        for chat in target_chats:
            messages: AsyncIterable = self.scripts_use_case.start_script(script_id)
            bots_mapping = sfc.bots_mapping
            bots_mapping = {key: await self.workers_use_case.get(value) for key, value in bots_mapping.items()}

            async for message in messages:
                await sleep(self._get_random_sleep())
                await self.workers_use_case.send_message(
                    chat_id=chat,
                    bot_id=bots_mapping[str(message.bot_index)].id,  # TODO: resolve fucking types
                    message=message.text,
                )
                logger.info(f"Message {message} sent to chat {chat}")

            logger.info(f"All messages from script {script_id} are sent to chat {chat}")
        logger.info(f"All messages from script {script_id} are sent to all chats")

    def _get_random_sleep(self):
        return randint(self.typing_and_sending_sleep_from, self.typing_and_sending_sleep_to)

    def execute(self):
        # active_scripts = await self.scripts_use_case
        ...