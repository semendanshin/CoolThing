from infrastructure.MockBotsService import MockBotsService


def get_bots_service() -> MockBotsService:
    return MockBotsService()
