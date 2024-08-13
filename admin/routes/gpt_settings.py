from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from abstractions.usecases.GPTSettingsUseCaseInterface import GPTSettingsUseCaseInterface
from dependencies.usecases.gpt_settings import get_gpt_settings_usecase
from domain.dto.gpt import GPTUpdateDTO, GPTCreateDTO
from forms.gpt_setting_create import create_gpt_setting_form
from forms.gpt_setting_update import update_gpt_setting_form

router = APIRouter(
    prefix="/gpt",
    tags=["gpt"],
)

templates = Jinja2Templates(directory='templates')


@router.get("")
async def get_gpts(
        request: Request,
        gpt_settings: GPTSettingsUseCaseInterface = Depends(get_gpt_settings_usecase)
) -> HTMLResponse:
    gpt_settings_list = await gpt_settings.get_all()
    return templates.TemplateResponse(
        request=request,
        name="gpt_settings.html",
        context={
            'gpt_settings': gpt_settings_list,
        }
    )


@router.get("/new")
async def get_new_gpt(
        request: Request,
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="new_gpt_setting.html",
    )


@router.get("/{gpt_id}")
async def get_gpt(
        gpt_id: str,
        request: Request,
        gpt_settings: GPTSettingsUseCaseInterface = Depends(get_gpt_settings_usecase),
) -> HTMLResponse:
    gpt_setting = await gpt_settings.get(gpt_id)
    return templates.TemplateResponse(
        request=request,
        name="gpt_setting.html",
        context={
            'gpt_setting': gpt_setting,
            'delete_url': f"/gpt/{gpt_setting.id}",
        }
    )


@router.post("")
async def create_gpt_backend(
        create_schema: GPTCreateDTO = Depends(create_gpt_setting_form),
        gpt_settings: GPTSettingsUseCaseInterface = Depends(get_gpt_settings_usecase),
) -> RedirectResponse:
    await gpt_settings.create(create_schema)
    return RedirectResponse(url='/gpt', status_code=303)


@router.post("/{gpt_id}")
async def update_gpt_backend(
        gpt_id: str,
        update_schema: GPTUpdateDTO = Depends(update_gpt_setting_form),
        gpt_settings: GPTSettingsUseCaseInterface = Depends(get_gpt_settings_usecase),
) -> RedirectResponse:
    await gpt_settings.update(gpt_id, update_schema)
    return RedirectResponse(url=f'/gpt/{gpt_id}', status_code=303)


@router.delete("/{gpt_id}")
async def delete_gpt_backend(
        gpt_id: str,
        gpt_settings: GPTSettingsUseCaseInterface = Depends(get_gpt_settings_usecase),
) -> RedirectResponse:
    await gpt_settings.delete(gpt_id)
    return RedirectResponse(url=f'/gpt', status_code=303)
