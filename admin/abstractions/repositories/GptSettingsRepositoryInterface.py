from abc import ABC

from abstractions.repositories import CRUDRepositoryInterface
from domain.dto.gpt import GPTCreateDTO, GPTUpdateDTO
from domain.models import GPT


class GptSettingsRepositoryInterface(
    CRUDRepositoryInterface[
        GPT, GPTCreateDTO, GPTUpdateDTO,
    ],
    ABC,
):
    ...
