from dataclasses import dataclass

from abstractions.repositories.CampaignRepositoryInterface import CampaignRepositoryInterface
from abstractions.repositories.WorkersRepositoryInterface import WorkersRepositoryInterface
from abstractions.repositories.GptSettingsRepositoryInterface import GptSettingsRepositoryInterface
from abstractions.repositories.ChatsRepositoryInterface import ChatsRepositoryInterface
from abstractions.usecases import BotsUseCaseInterface
from domain.models import Worker as WorkerModel
from domain.models import Campaign as CampaignModel
from domain.models import Chat as ChatModel
from domain.models import GPT as GPTModel
from domain.schemas.bots import ManagerBotDetails, ParserBotDetails, ManagerBotOverview, ParserBotOverview


@dataclass
class BotsUseCase(
    BotsUseCaseInterface,
):
    workers_repo: WorkersRepositoryInterface
    campaign_repo: CampaignRepositoryInterface
    gpt_repo: GptSettingsRepositoryInterface
    chats_repo: ChatsRepositoryInterface

    async def get_bot(self, bot_username: str) -> ManagerBotDetails | ParserBotDetails:
        worker = await self.workers_repo.get_by_username(bot_username)
        match worker.role:
            case 'manager':
                return await self.worker_to_manager_details(worker)
            case 'parser':
                return await self.worker_to_parser_details(worker)

    async def get_manager_bots(self) -> list[ManagerBotOverview]:
        bots = await self.workers_repo.get_by_role(role='manager')
        return [await self.worker_to_manager_overview(bot) for bot in bots]

    async def get_parser_bots(self) -> list[ParserBotOverview]:
        bots = await self.workers_repo.get_by_role(role='parser')
        return [await self.worker_to_parser_overview(bot) for bot in bots]

    async def connect_bot_by_code(self, code: str) -> bool:
        return True

    async def connect_bot_by_password(self, password: str) -> bool:
        return True

    async def _get_worker_campaign(self, worker: WorkerModel) -> CampaignModel:
        return await self.campaign_repo.get(worker.campaign_id)

    async def _get_worker_gpt(self, worker: WorkerModel, campaign: CampaignModel = None) -> GPTModel:
        if not campaign:
            campaign = await self._get_worker_campaign(worker)
        return await self.gpt_repo.get(campaign.gpt_settings_id)

    async def _get_worker_chats(self, worker: WorkerModel) -> list[ChatModel]:
        return await self.chats_repo.get_by_worker_id(worker.id)

    async def worker_to_manager_overview(self, worker: WorkerModel) -> ManagerBotOverview:
        campaign = await self._get_worker_campaign(worker)
        return await self._worker_to_manager_overview(worker, campaign)

    async def _worker_to_manager_overview(self, worker: WorkerModel, campaign: CampaignModel) -> ManagerBotOverview:
        return ManagerBotOverview(
            nickname=worker.username,
            scope=campaign.scope,
            proxy=worker.proxy if worker.proxy else 'No proxy',
            proxy_status=worker.status == 'active',
            unread_messages=0,
            messages_count=0,
            chats_ratio='0/0',
        )

    async def worker_to_manager_details(self, worker: WorkerModel) -> ManagerBotDetails:
        campaign = await self._get_worker_campaign(worker)
        gpt = await self.gpt_repo.get(campaign.gpt_settings_id)
        chats = await self.chats_repo.get_by_worker_id(worker.id)
        return await self._worker_to_manager_details(
            worker=worker,
            campaign=campaign,
            chats=chats,
            gpt=gpt,
        )

    async def _worker_to_manager_details(self, worker: WorkerModel, campaign: CampaignModel, chats: list[ChatModel],
                                         gpt: GPTModel) -> ManagerBotDetails:
        return ManagerBotDetails(
            avatar='',
            nickname=worker.username,
            bio=worker.bio,
            scope=campaign.scope,
            proxy=worker.proxy if worker.proxy else 'No proxy',
            chats_count=len(chats),
            api_key=gpt.token,
            chatgpt_model=gpt.model,
            chatgpt_assistant=gpt.assistant,
        )

    async def worker_to_parser_overview(self, worker: WorkerModel) -> ParserBotOverview:
        campaign = await self._get_worker_campaign(worker)
        return await self._worker_to_parser_overview(
            worker=worker,
            campaign=campaign,
        )

    async def _worker_to_parser_overview(self, worker: WorkerModel, campaign: CampaignModel) -> ParserBotOverview:
        return ParserBotOverview(
            nickname=worker.username,
            scope=campaign.scope,
            proxy=worker.proxy if worker.proxy else 'No proxy',
            proxy_status=worker.status == 'active',
            positive_keywords=campaign.plus_keywords,
            negative_keywords=campaign.minus_keywords,
            chats=campaign.chats,
        )

    async def worker_to_parser_details(self, worker: WorkerModel) -> ParserBotDetails:
        campaign = await self._get_worker_campaign(worker)
        return await self._worker_to_parser_details(
            worker=worker,
            campaign=campaign,
        )

    async def _worker_to_parser_details(self, worker: WorkerModel, campaign: CampaignModel) -> ParserBotDetails:
        return ParserBotDetails(
            avatar='',
            nickname=worker.username,
            bio=worker.bio,
            scope=campaign.scope,
            proxy=worker.proxy if worker.proxy else 'No proxy',
            positive_keywords=campaign.plus_keywords,
            negative_keywords=campaign.minus_keywords,
            chats=campaign.chats,
        )
