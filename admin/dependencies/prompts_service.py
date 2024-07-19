from infrastructure.MockPromptsService import MockPromptsService


def get_prompts_service() -> MockPromptsService:
    return MockPromptsService()
