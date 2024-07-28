from dataclasses import dataclass

from openai import OpenAI

from abstractions.repositories.gpt import GPTRepositoryInterface
from domain.models import Message


@dataclass
class GPTRepository(GPTRepositoryInterface):
    api_key: str
    model: str

    service_prompt: str = """
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


@dataclass
class AssistantRepository(GPTRepositoryInterface):
    api_key: str
    model: str

    assistant_id: str

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
        assistant = self.openai.beta.assistants.retrieve(self.assistant_id)
        thread = self.openai.beta.threads.create(
            messages=self.prepare_messages(messages),
        )
        run = self.openai.beta.threads.runs.create_and_poll(
            assistant_id=assistant.id,
            thread_id=thread.id,
        )
        thread_messages = self.openai.beta.threads.messages.list(
            thread_id=thread.id,
            run_id=run.id,
            limit=1
        )
        message = thread_messages.__iter__().__next__()
        return message.content[0].text.value

