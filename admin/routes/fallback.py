from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from .common import templates

router = APIRouter(
    prefix='/fallback',
    tags=['Fallback'],
)


@router.get("")
async def get_fallback(
        request: Request,
        msg: str = None,
) -> HTMLResponse:
    print(msg)
    return templates.TemplateResponse(
        request=request,
        name='fallback.html',
        context={
            'error': msg or 'Something went wrong. Please try again later.',
        },
    )
