from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from abstractions.AbstractPromptsService import AbstractPromptsService
from dependencies.prompts_service import get_prompts_service

router = APIRouter(
    prefix='/prompts',
    tags=['Prompts'],
)

templates = Jinja2Templates(directory='templates')

@router.get("")
async def get_all_prompts(
        request: Request,
        prompts: AbstractPromptsService = Depends(get_prompts_service),
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name='prompts.html',
        context={
            'prompts': await prompts.get_all_prompts(),
        },
    )

