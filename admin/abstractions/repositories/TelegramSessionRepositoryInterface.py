from abc import abstractmethod, ABC


class SessionRepositoryException(Exception):
    pass


class AppIdNotFoundException(SessionRepositoryException):
    pass


class TwoFARequiredException(SessionRepositoryException):
    pass


class InvalidCodeException(SessionRepositoryException):
    pass


class InvalidPasswordException(SessionRepositoryException):
    pass


class TelegramSessionRepositoryInterface(ABC):
    @abstractmethod
    async def send_code(self, app_id: int, app_hash: str, phone: str, proxy: str) -> None:
        pass

    @abstractmethod
    async def authorize(self, app_id: int, code: str) -> str:
        pass

    @abstractmethod
    async def authorize_2fa(self, app_id: int, password: str) -> str:
        pass
