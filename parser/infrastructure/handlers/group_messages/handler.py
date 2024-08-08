import logging
from dataclasses import dataclass

from nltk.stem.snowball import SnowballStemmer
from telethon import TelegramClient, events

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

    async def react_to_message(self, event: events.NewMessage.Event):
        username = (await event.get_sender()).username
        logger.debug(f"{event.message.text} from {username} in {event.chat.id}")
        result = self._is_relevant(event.message.text)
        if result and username:
            logger.info(f"Relevant message: {event.message.text} from {username} in {event.chat.id}")
            await self.event_use_cases.publish(
                NewTargetMessage(
                    chat_id=event.chat.id,
                    username=username,
                    message=event.message.text,
                    campaign_id=self.campaign_id,
                    worker_id=self.worker_id,
                )
            )

    def register_handlers(self, app: TelegramClient):
        logger.info("Registering handlers. Chats: %s", self.chats)

        def _filter(event: events.NewMessage.Event):
            return event.message.text and (int(str(event.chat_id).removeprefix("-100")) in self.chats)

        app.on(
            events.NewMessage(
                incoming=True,
                outgoing=True,
                func=_filter
            )
        )(self.react_to_message)
