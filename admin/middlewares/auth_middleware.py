from fastapi import Request
from fastapi.responses import RedirectResponse

from dependencies.usecases.auth import get_auth_use_case
from domain.schemas.auth import Tokens


async def check_for_auth(
        request: Request,
        call_next,
):
    if request.url.path == "/auth" or request.url.path.startswith("/static"):
        response = await call_next(request)
        return response

    tokens = Tokens(
        access_token=request.cookies.get("access_token", ""),
        # refresh_token=request.cookies.get("refresh_token", ""),
    )

    auth_use_case = get_auth_use_case()
    if not await auth_use_case.check_tokens(tokens):
        print("not authorized")
        return RedirectResponse(url='/auth', status_code=303)
    else:
        print("authorized")
        response = await call_next(request)
        return response
