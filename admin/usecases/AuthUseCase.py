import jwt

from datetime import datetime, timedelta, timezone

from abstractions.usecases.AuthUseCaseInterface import AuthUseCaseInterface
from config import AuthSettings
from domain.schemas.auth import Credentials, Tokens
from usecases.exceptions import WrongCredentialsException


class AuthUseCase(AuthUseCaseInterface):
    def __init__(self, auth_settings: AuthSettings):
        self.auth_settings = auth_settings

    def get_access_token_lifetime_seconds(self) -> int:
        return self.auth_settings.access_token_lifetime_seconds

    def check_credentials(self, credentials: Credentials) -> bool:
        if credentials.auth_code == self.auth_settings.code.get_secret_value():
            return True

        return False

    def _generate_tokens(self, credentials: Credentials) -> Tokens:
        now = datetime.now(tz=timezone.utc)
        access_expires = now + timedelta(seconds=self.auth_settings.access_token_lifetime_seconds)
        access_token = jwt.encode(
            payload={
                'exp': access_expires,
            },
            key=self.auth_settings.secret_key.get_secret_value(),
            algorithm='HS256'
        )

        return Tokens(
            access_token=access_token,
        )

    async def create_tokens(self, credentials: Credentials) -> Tokens:
        if self.check_credentials(credentials):
            return self._generate_tokens(credentials)
        else:
            print("wrong creds")
            raise WrongCredentialsException()

    async def check_tokens(self, tokens: Tokens) -> bool:
        try:
            jwt.decode(
                jwt=tokens.access_token,
                key=self.auth_settings.secret_key.get_secret_value(),
                algorithms=['HS256']
            )
            return True
        except jwt.ExpiredSignatureError:
            print("access expired")
            pass
        except Exception as e:
            print(e)
            pass

        return False
