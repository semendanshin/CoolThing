from abc import abstractmethod, ABC


class MessagesUseCaseInterface(ABC):
    @abstractmethod
    async def send_and_save_message(self, chat_id: str, text: str) -> None:
        pass
