import logging
from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from abstractions.usecases.GPTSettingsUseCaseInterface import GPTSettingsUseCaseInterface
from dependencies.usecases.gpt_settings import get_gpt_settings_usecase
from domain.models import GPT as GPTModel

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/gpts",
    tags=["gpts"],
)


class GPT(BaseModel):
    id: UUID
    updated_at: datetime
    created_at: datetime
    model: Optional[str] = None
    token: str
    proxy: Optional[str] = None
    assistant: Optional[str] = None
    service_prompt: str

    @classmethod
    def from_domain(cls, model: GPTModel) -> "GPT":
        return GPT(
            id=UUID(model.id),
            model=model.model,
            token=model.token,
            proxy=model.proxy,
            assistant=model.assistant,
            service_prompt=model.service_prompt,
            updated_at=model.updated_at,
            created_at=model.created_at,
        )


@router.get("")
async def get_gpts(
        gpt_settings_use_case: GPTSettingsUseCaseInterface = Depends(get_gpt_settings_usecase),
) -> list[GPT]:
    settings = await gpt_settings_use_case.get_all()
    result = list(map(lambda s: GPT.from_domain(s), settings))
    return result
