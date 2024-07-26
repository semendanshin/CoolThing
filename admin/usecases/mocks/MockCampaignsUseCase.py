from abstractions.usecases.CampaingsUseCaseInterface import CampaignsUseCaseInterface
from domain.dto.campaign import CampaignUpdateDTO
from domain.models import Campaign as CampaignModel


class MockCampaignsUseCase(CampaignsUseCaseInterface):
    async def update_campaign(self, campaign_id: str, schema: CampaignUpdateDTO) -> list[CampaignModel]:
        print(f"Updating campaign {campaign_id} with schema {schema.asdict()}")

    async def get_campaign(self, campaign_id: str) -> CampaignModel:
        return CampaignModel(
            welcome_message="Welcome message",
            chats=['chat1', 'chat2'],
            plus_keywords=["plus"],
            minus_keywords=["minus"],
            gpt_settings_id="gpt_settings_id",
            scope="scope"
        )

    async def get_campaigns(self) -> list[CampaignModel]:
        return [
            CampaignModel(
                welcome_message="Welcome message",
                chats=['chat1', 'chat2'],
                plus_keywords=["plus"],
                minus_keywords=["minus"],
                gpt_settings_id="gpt_settings_id",
                scope="scope"
            ),
            CampaignModel(
                welcome_message="Welcome message",
                chats=['chat1', 'chat2'],
                plus_keywords=["plus"],
                minus_keywords=["minus"],
                gpt_settings_id="gpt_settings_id",
                scope="scope"
            ),
            CampaignModel(
                welcome_message="Welcome message",
                chats=['chat1', 'chat2'],
                plus_keywords=["plus"],
                minus_keywords=["minus"],
                gpt_settings_id="gpt_settings_id",
                scope="scope"
            ),
        ]
