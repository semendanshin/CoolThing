from abc import ABC
from dataclasses import dataclass
from typing import Optional

from abstractions.repositories import CRUDRepositoryInterface
from domain.models import GPT


@dataclass
class GPTCreateDTO:
    id: str
    model: str
    assistant: Optional[str]
    token: str


@dataclass
class GPTUpdateDTO:
    id: str
    model: Optional[str]
    assistant: Optional[str]
    token: Optional[str]


class GPTRepositoryInterface(
    CRUDRepositoryInterface[GPT, GPTCreateDTO, GPTUpdateDTO], ABC
):
    pass
