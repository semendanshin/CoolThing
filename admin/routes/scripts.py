import json

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse

from dependencies.usecases.scripts import get_scripts_use_case
from domain.dto.script import ScriptCreateDTO, ScriptUpdateDTO, ScriptForCampaignCreateDTO
from .active_scripts import router as asrouter
from .common import templates

router = APIRouter(
    prefix="/scripts",
    tags=["Scripts"],
)
router.include_router(asrouter)


@router.get("")
async def get_scripts(
        request: Request,
        # scripts: ScriptsUseCaseInterface = Depends(get_scripts_use_case),
):
    scripts = await get_scripts_use_case().get_scripts()
    return templates.TemplateResponse(
        request=request,
        name="scripts.html",
        context={
            'scripts': scripts,
        }
    )


@router.get("/new")
async def get_create_script(
        request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name='new_script.html',
        context={

        }
    )


@router.get("/bots-count/{script_id}")
async def get_script_bots_count(
        script_id: str,
) -> int:
    script = await get_scripts_use_case().get_script(script_id)
    print(script.messages)
    res = max([x.bot_index for x in script.messages])
    print(res)
    return res


@router.get("/{script_id}")
async def get_script(
        script_id: str,
        request: Request,
        # scripts: ScriptsUseCaseInterface = Depends(get_scripts_use_case),
):
    if script_id == 'bots-count':
        raise HTTPException(status_code=422, detail="It's not uuid, check your code")

    script = await get_scripts_use_case().get_script(script_id)
    messages_object_string = json.dumps([x.__dict__ for x in script.messages])
    # messages_object_string = messages_object_string.replace('`', r'\`')
    print(messages_object_string)
    return templates.TemplateResponse(
        request=request,
        name='update_script.html',
        context={
            'script': script,
            'delete_url': f'/scripts/{script_id}',
            'messages_object': messages_object_string,
        }
    )


@router.post("")
async def create_script(
        script: ScriptCreateDTO,
        # scripts: ScriptsUseCaseInterface = Depends(get_scripts_use_case),
) -> RedirectResponse:
    await get_scripts_use_case().create_script(script)
    return RedirectResponse(url="/scripts", status_code=303)


@router.put("/{script_id}")
async def update_script(
        script_id: str,
        script: ScriptUpdateDTO,
        # scripts: ScriptsUseCaseInterface = Depends(get_scripts_use_case),
):
    await get_scripts_use_case().update_script(script_id, script)
    return RedirectResponse(url=f"/scripts/{script_id}", status_code=303)


@router.delete("/{script_id}")
async def delete_script(
        script_id: str,
        # scripts: ScriptsUseCaseInterface = Depends(get_scripts_use_case),
):
    await get_scripts_use_case().delete_script(script_id)
    return RedirectResponse(url="/scripts", status_code=303)


@router.post("/activate")
async def activate_script(
        script_for_campaign: ScriptForCampaignCreateDTO,
        # scripts_use_case: ScriptsUseCaseInterface = Depends(get_scripts_use_case),
):
    scripts_use_case = get_scripts_use_case()
    await scripts_use_case.activate_script(script_for_campaign)

    # raise HTTPException(status_code=500, detail=f"Something went wrong while processing your request. Detail: {e}")
