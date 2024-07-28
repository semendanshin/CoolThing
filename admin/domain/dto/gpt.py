from dataclasses import dataclass
from typing import Optional


@dataclass(kw_only=True)
class GPTCreateDTO:
    model: str
    assistant: str
    token: str
    service_prompt: str


@dataclass(kw_only=True)
class GPTUpdateDTO:
    id: str
    model: Optional[str]
    assistant: Optional[str]
    token: Optional[str]
    service_prompt: Optional[str]
