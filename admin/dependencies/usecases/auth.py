from abstractions.usecases.AuthUseCaseInterface import AuthUseCaseInterface
from config import settings
from usecases.AuthUseCase import AuthUseCase


def get_auth_use_case() -> AuthUseCaseInterface:
    return AuthUseCase(auth_settings=settings.auth)
