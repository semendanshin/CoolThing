import logging
from dataclasses import dataclass

from nltk.stem.snowball import SnowballStemmer
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from domain.new_target_message import NewTargetMessage
from usecases.events import EventUseCases

logger = logging.getLogger(__name__)


@dataclass
class GroupMessageHandler:
    chats: list[int]
    positive_key_words: set[str]
    negative_key_words: set[str]

    worker_id: str
    campaign_id: str

    event_use_cases: EventUseCases

    punctuation: str = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    stemmer: SnowballStemmer = SnowballStemmer("russian")

    def _is_relevant(self, text: str) -> bool:
        # clean text by removing punctuation, lowercasing, lemmatizing
        text = text.lower()
        text = text.translate(str.maketrans('', '', self.punctuation))
        text = set([self.stemmer.stem(word) for word in text.split()])
        logger.debug(f"Cleaned text: {text}")

        # check if text does not contain negative keywords
        if text & self.negative_key_words or not text & self.positive_key_words:
            return False

        return True

    async def react_to_message(self, client, message: Message):
        logger.debug(f"{message.text} from {message.from_user.username} in {message.chat.id}")
        result = self._is_relevant(message.text)
        # await client.send_message(
        #     message.chat.id,
        #     f"Это сообщение {'актуально' if result else 'неактуально'}"
        # )
        if result and message.from_user.username:
            logger.info(f"Relevant message: {message.text} from {message.from_user.username} in {message.chat.id}")
            await self.event_use_cases.publish(
                NewTargetMessage(
                    chat_id=message.chat.id,
                    username=message.from_user.username,
                    message=message.text,
                    campaign_id=self.campaign_id,
                    worker_id=self.worker_id,
                )
            )

    def register_handlers(self, client: Client):
        client.add_handler(
            MessageHandler(
                self.react_to_message,
                filters.chat(self.chats) & filters.text,
            )
        )
