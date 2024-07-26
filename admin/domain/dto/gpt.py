from dataclasses import dataclass


@dataclass(kw_only=True)
class GPTCreateDTO:
    model: str
    assistant: str
    token: str
    service_prompt: str


@dataclass(kw_only=True)
class GPTUpdateDTO:
    model: str
    assistant: str
    token: str
    service_prompt: str
