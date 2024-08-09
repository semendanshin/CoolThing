from dataclasses import dataclass

import httpx
from httpx import Proxy
from openai import AsyncOpenAI as OpenAI

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

    proxy: str = None

    def __post_init__(self):
        if self.proxy:
            httpx_client = httpx.AsyncClient(proxy=Proxy(self.proxy))
        else:
            httpx_client = None
        self.openai = OpenAI(
            api_key=self.api_key,
            http_client=httpx_client
        )

    @staticmethod
    def prepare_messages(messages: list[Message]) -> list[dict[str, str]]:
        return [
            {"role": "assistant" if message.is_outgoing else "user", "content": message.text}
            for message in messages
        ]

    async def generate_response(self, messages: list[Message]) -> str:
        return (await self.openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.service_prompt},
            ] + self.prepare_messages(messages),
            stream=False,
        )).choices[0].message.content


@dataclass
class AssistantRepository(GPTRepositoryInterface):
    api_key: str
    model: str

    assistant_id: str

    proxy: str = None

    def __post_init__(self):
        if self.proxy:
            httpx_client = httpx.AsyncClient(proxy=Proxy(self.proxy))
        else:
            httpx_client = None
        self.openai = OpenAI(
            api_key=self.api_key,
            http_client=httpx_client
        )

    @staticmethod
    def prepare_messages(messages: list[Message]) -> list[dict[str, str]]:
        return [
            {"role": "assistant" if message.is_outgoing else "user", "content": message.text}
            for message in messages
        ]

    async def generate_response(self, messages: list[Message]) -> str:
        assistant = await self.openai.beta.assistants.retrieve(self.assistant_id)
        thread = await self.openai.beta.threads.create(
            messages=self.prepare_messages(messages),
        )
        run = await self.openai.beta.threads.runs.create_and_poll(
            assistant_id=assistant.id,
            thread_id=thread.id,
        )
        thread_messages = await self.openai.beta.threads.messages.list(
            thread_id=thread.id,
            run_id=run.id,
            limit=1
        )
        message = await thread_messages.__aiter__().__anext__()
        await self.openai.beta.threads.delete(thread.id)
        return message.content[0].text.value

