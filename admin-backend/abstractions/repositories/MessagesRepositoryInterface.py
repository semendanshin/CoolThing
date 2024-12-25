from abc import ABC, abstractmethod

from abstractions.repositories import CRUDRepositoryInterface
from domain.dto.message import MessageCreateDTO, MessageUpdateDTO
from domain.models import Message


class MessagesRepositoryInterface(
    CRUDRepositoryInterface[
        Message, MessageCreateDTO, MessageUpdateDTO,
    ],
    ABC,
):
    pass
