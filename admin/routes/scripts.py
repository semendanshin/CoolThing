from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates

router = APIRouter(
    prefix='/scripts',
    tags=['Scripts']
)

templates = Jinja2Templates(directory='templates')


@router.get("")
async def get_scripts(
        request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name='new_script.html',
        context={

        }
    )
