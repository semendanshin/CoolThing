from typing import Optional

from pydantic import BaseModel


class GPTSettings(BaseModel):
    id: str
    model: str
    token: str
    assistant: Optional[str] = ""
    service_prompt: Optional[str] = ""


class GPTSettingsCreate(BaseModel):
    model: str
    token: str
    assistant: Optional[str] = ""
    service_prompt: Optional[str] = ""


class GPTSettingsUpdate(BaseModel):
    id: str
    model: Optional[str] = None
    token: Optional[str] = None
    assistant: Optional[str] = None
    service_prompt: Optional[str] = None
