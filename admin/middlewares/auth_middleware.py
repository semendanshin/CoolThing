from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.datastructures import URL

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
        destination_url = request.url.path
        url = URL("/auth").include_query_params(destination=destination_url)
        return RedirectResponse(url=url, status_code=303)
    else:
        response = await call_next(request)
        return response
