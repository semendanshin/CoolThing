import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass(kw_only=True)
class GPTCreateDTO:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    model: str
    assistant: str
    token: str
    service_prompt: str


@dataclass(kw_only=True)
class GPTUpdateDTO:
    id: str = None
    model: Optional[str]
    assistant: Optional[str]
    token: Optional[str]
    service_prompt: Optional[str]
