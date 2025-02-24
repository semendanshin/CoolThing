from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from .common import templates

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/base")
async def get_base(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name='base.html',
        context={
        },
    )


@router.get("")
async def get_dashboard(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name='dashboard.html',
        context={
        },
    )
