from dataclasses import dataclass

from abstractions.repositories.CampaignRepositoryInterface import CampaignRepositoryInterface
from abstractions.repositories.ScriptsForCampaignRepositoryInterface import ScriptsForCampaignRepositoryInterface
from abstractions.repositories.ScriptsRepositoryInterface import ScriptsRepositoryInterface
from abstractions.repositories.WorkersRepositoryInterface import WorkersRepositoryInterface


@dataclass
class MetricsService:
    scripts_repo: ScriptsRepositoryInterface
    scripts_for_campaign_repo: ScriptsForCampaignRepositoryInterface
    campaign_repo: CampaignRepositoryInterface
    workers_repo: WorkersRepositoryInterface

    async def get_today_scripts(self):
        return self.scripts_repo.get_scripts_by_n_last_days(n=1)

    async def get_week_scripts(self):
        return self.scripts_repo.get_scripts_by_n_last_days(n=7)

    async def get_month_scripts(self):
        return self.scripts_repo.get_scripts_by_n_last_days(n=30)

    async def get_all_scripts(self):
        return self.scripts_repo.get_all()

    async def get_active_scripts(self):
        return self.scripts_repo.get_active_scripts()

    async def get_grouped_scripts_by_campaign(self):
        return self.scripts_for_campaign_repo.get_grouped_scripts_by_campaign()

    async def get_grouped_scripts_by_bots(self):
        return self.scripts_for_campaign_repo.get_grouped_scripts_by_bots()

    async def get_grouped_scripts_by_chats(self):
        return self.scripts_for_campaign_repo.get_grouped_scripts_by_chats()

    async def get_bots_statistics(self):
        return self.workers_repo.get_bots_statistics()

    async def get_chats_statistics(self, n: int):
        return self.scripts_for_campaign_repo.get_chats_statistics_by_n_last_days(n=n)
