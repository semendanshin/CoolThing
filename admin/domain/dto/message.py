from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(kw_only=True)
class MessageCreateDTO:
    id: str = field(default_factory=lambda: str(uuid4()))
    chat_id: str
    text: str
    is_outgoing: bool


@dataclass(kw_only=True)
class MessageUpdateDTO:
    id: str = None
    text: str
