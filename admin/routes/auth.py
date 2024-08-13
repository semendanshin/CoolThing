from fastapi import APIRouter, Depends, Body
from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse
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
        destination: str = "/dashboard",
):
    return templates.TemplateResponse(
        request=request,
        name='auth.html',
        context={
            "destination": destination
        },
    )


@router.post("")
async def validate_auth_code_backend(
        credentials: Credentials = Depends(auth_code_form),
        auth_use_case: AuthUseCaseInterface = Depends(get_auth_use_case),
) -> JSONResponse:
    try:
        tokens = await auth_use_case.create_tokens(credentials)
        response = JSONResponse(content={"status": "ok"}, status_code=200)
        response.set_cookie(key="access_token", value=tokens.access_token)
        # response.set_cookie(key="refresh_token", value=tokens.refresh_token)
        return response
    except WrongCredentialsException:
        return JSONResponse(content={"status": "error", "message": "Wrong credentials"}, status_code=400)
