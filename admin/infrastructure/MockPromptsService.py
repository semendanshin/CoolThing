from abstractions.AbstractPromptsService import AbstractPromptsService
from domain.prompts import Prompt


class MockPromptsService(AbstractPromptsService):
    async def get_all_prompts(self) -> list[Prompt]:
        return [
            Prompt(
                aim='Check for interest',
                prompt='Some prompt to check interest'
            ),
            Prompt(
                aim='Filter prompt',
                prompt='Some prompt to filter'
            ),
            Prompt(
                aim='Positive and negative keywords vary',
                prompt='Prompt to vary keywords'
            ),
        ]