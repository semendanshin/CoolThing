from typing import Optional

from pydantic import BaseModel


class GPTSettings(BaseModel):
    id: str
    name: str
    model: str
    token: str
    assistant: Optional[str] = ""
    service_prompt: Optional[str] = ""


class GPTSettingsCreate(BaseModel):
    model: str
    name: str
    token: str
    assistant: Optional[str] = ""
    service_prompt: Optional[str] = ""


class GPTSettingsUpdate(BaseModel):
    id: str
    name: Optional[str] = None
    model: Optional[str] = None
    token: Optional[str] = None
    assistant: Optional[str] = None
    service_prompt: Optional[str] = None
