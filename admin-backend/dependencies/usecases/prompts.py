from usecases.mocks.MockPromptsUseCase import MockPromptsUseCase


def get_prompts_service() -> MockPromptsUseCase:
    return MockPromptsUseCase()
