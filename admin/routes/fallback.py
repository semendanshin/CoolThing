from fastapi import APIRouter, Request

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/fallback',
    tags=['Fallback'],
)

templates = Jinja2Templates(directory='templates')


@router.get("")
async def get_fallback(
        request: Request,
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name='fallback.html',
        context={
            'error': 'Something went wrong. Please try again later.',
        },
    )