from domain.dto.worker import WorkerCreateDTO, WorkerUpdateDTO
from domain.models import Worker
# from domain.schemas.bots import ManagerBotOverview, ParserBotOverview, ManagerBotDetails, ParserBotDetails
from abstractions.usecases import BotsUseCaseInterface


class MockBotsUseCase(BotsUseCaseInterface):
    async def get_bot(self, bot_id: str) -> Worker:
        pass

    async def update(self, bot_id: str, schema: WorkerUpdateDTO) -> None:
        pass

    async def send_code(self, app_id: int, app_hash: str, phone: str) -> None:
        pass

    async def authorize(self, app_id: int, code: str) -> str:
        pass

    async def authorize_2fa(self, app_id: int, password: str) -> str:
        pass

    async def create(self, schema: WorkerCreateDTO) -> None:
        pass

    parsers = False

    async def get_all_bots(self) -> list[Worker]:
        return [
            Worker(
                id="id",
                app_id="app_id",
                app_hash="app_hash",
                session_string="session_string",
                proxy="0.0.0.0",
                campaign_id='1',
                role='Manager',
                status='active',
                username='@adsforyou',
                bio='basic bio',
            ),
            Worker(
                id='id',
                app_id='app_id',
                app_hash='app_hash',
                session_string="session_string",
                proxy="0.0.0.0",
                campaign_id='2',
                role='Parser',
                status='active',
                username='@newnickname',
                bio='basic bio',
            ),
        ]