from dataclasses import dataclass

from openai import OpenAI

from abstractions.repositories.gpt import GPTRepositoryInterface
from domain.models import Message


@dataclass
class GPTRepository(GPTRepositoryInterface):
    api_key: str
    model: str

    service_prompt = """
    Ты - менеджер, занимающийся прогревом клиентов для нашего агентства недвижимости.
    Тебе предстоит общаться с людьми, которые в тематических чатах писали о заинтересованы в аренде или покупке жилья. 
    Приветственно сообщение от тебя уже отправлено. 
    Я буду присылать тебе  сообщения от клиентов, а тебе нужно придумать ответ на это сообщение.
    """

    def __post_init__(self):
        self.openai = OpenAI(
            api_key=self.api_key,
        )

    @staticmethod
    def prepare_messages(messages: list[Message]) -> list[dict[str, str]]:
        return [
            {"role": "assistant" if message.is_outgoing else "user", "content": message.text}
            for message in messages
        ]

    async def generate_response(self, messages: list[Message]) -> str:
        return self.openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.service_prompt},
            ] + self.prepare_messages(messages),
            stream=False,
        ).choices[0].message.content
