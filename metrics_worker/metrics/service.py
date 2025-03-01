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
        return await self.scripts_repo.get_scripts_by_n_last_days(n=1)

    async def get_week_scripts(self):
        return await self.scripts_repo.get_scripts_by_n_last_days(n=7)

    async def get_month_scripts(self):
        return await self.scripts_repo.get_scripts_by_n_last_days(n=30)

    async def get_all_scripts(self):
        return await self.scripts_repo.get_all()

    async def get_active_scripts(self):
        return await self.scripts_repo.get_active_scripts()

    async def get_grouped_scripts_by_campaign(self):
        return await self.scripts_for_campaign_repo.get_grouped_scripts_by_campaign()

    async def get_grouped_scripts_by_bots(self):
        return await self.scripts_for_campaign_repo.get_grouped_scripts_by_bots()

    async def get_grouped_scripts_by_chats(self):
        # Step 1: Get grouped data from MongoDB
        grouped_chats = await self.scripts_for_campaign_repo.get_grouped_scripts_by_chats()

        # Step 2: Extract campaign IDs
        campaign_ids = [entry["id"] for entry in grouped_chats]

        # Step 3: Fetch campaign names from PostgreSQL
        campaign_names = await self.campaign_repo.get_campaign_names_by_ids(campaign_ids)

        # Step 4: Append campaign names to the results
        for entry in grouped_chats:
            campaign_id = entry["id"]
            entry["campaign_name"] = campaign_names.get(campaign_id, "Unknown Campaign")

        print(grouped_chats)

        return grouped_chats

    async def get_bots_statistics(self):
        return await self.workers_repo.get_bots_statistics()

    async def get_chats_statistics(self, n: int):
        return await self.scripts_for_campaign_repo.get_chats_statistics_by_n_last_days(n=n)
