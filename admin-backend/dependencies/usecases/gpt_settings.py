from abstractions.usecases.GPTSettingsUseCaseInterface import GPTSettingsUseCaseInterface
from dependencies.repositories.gpt import get_gpt_repository
from usecases.GPTSettingsUseCase import GPTSettingsUseCase


def get_gpt_settings_usecase() -> GPTSettingsUseCaseInterface:
    return GPTSettingsUseCase(
        repository=get_gpt_repository()
    )
