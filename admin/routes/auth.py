from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from abstractions.usecases.AuthUseCaseInterface import AuthUseCaseInterface
from dependencies.usecases.auth import get_auth_use_case
from domain.schemas.auth import Credentials
from forms.auth_code_form import auth_code_form
from usecases.exceptions import WrongCredentialsException

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

templates = Jinja2Templates(directory='templates')


@router.get("")
async def get_login_page(
        request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name='auth.html',
        context={},
    )


@router.post("")
async def get_auth_code(
        credentials: Credentials = Depends(auth_code_form),
        auth_use_case: AuthUseCaseInterface = Depends(get_auth_use_case),
):
    try:
        tokens = await auth_use_case.create_tokens(credentials)
        response = RedirectResponse(url='/dashboard', status_code=303)
        response.set_cookie(key="access_token", value=tokens.access_token)
        # response.set_cookie(key="refresh_token", value=tokens.refresh_token)
        return response
    except WrongCredentialsException:
        return RedirectResponse(url='/auth', status_code=303)
