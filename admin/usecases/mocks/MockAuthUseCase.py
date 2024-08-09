from abstractions.usecases.AuthUseCaseInterface import AuthUseCaseInterface
from domain.schemas.auth import Credentials, Tokens


class MockAuthUseCase(AuthUseCaseInterface):
    def get_access_token_lifetime_seconds(self) -> int:
        return 60 * 60

    def check_credentials(self, credentials: Credentials) -> bool:
        if credentials.auth_code == "123":
            return True
        else:
            return False

    async def create_tokens(self, credentials: Credentials) -> Tokens:
        if self.check_credentials(credentials):
            return Tokens(
                access_token="access_token",
            )
        else:
            return Tokens(
                access_token="invalid_access_token",
            )

    async def check_tokens(self, tokens: Tokens) -> bool:
        if tokens.access_token == "access_token":
            return True
        else:
            return False
