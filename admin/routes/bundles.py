from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from dependencies.usecases.bundles import get_bundles_use_case
from domain.dto.bundle import BundleCreateDTO, BundleUpdateDTO
from routes.common import templates

router = APIRouter(
    prefix='/bundles',
    tags=['Bundles'],
)


@router.get('')
async def get_all_bundles(
        request: Request,
) -> HTMLResponse:
    bundles = await get_bundles_use_case().get_bundles()
    return templates.TemplateResponse(
        name='bundles.html',
        request=request,
        context={
            'bundles': bundles,
        }
    )


@router.get('/new')
async def get_create_bundle(
        request: Request,
) -> RedirectResponse:
    return templates.TemplateResponse(
        name='new_bundle.html',
        request=request,
        context={

        },
    )


@router.get("/{bundle_id}")
async def get_bundle(
        request: Request,
        bundle_id: str,
) -> HTMLResponse:
    bundle = await get_bundles_use_case().get_bundle(bundle_id=bundle_id)
    return templates.TemplateResponse(
        name='update_bundle.html',
        request=request,
        context={
            'bundle': bundle,
            'delete_url': f'/bundles/{bundle.id}',
        },
    )


@router.post("")
async def create_bundle(
        create_schema: BundleCreateDTO,
):
    await get_bundles_use_case().create(create_schema)
    return RedirectResponse(url='/bundles', status_code=303)


@router.delete("/{bundle_id}")
async def delete_bundle(
        bundle_id: str,
):
    await get_bundles_use_case().delete(bundle_id)
    return RedirectResponse(url='/bundles', status_code=303)


@router.put("/{bundle_id}")
async def update_bundle(
        bundle_id: str,
        update_schema: BundleUpdateDTO
):
    await get_bundles_use_case().update(bundle_id=bundle_id, schema=update_schema)
    return RedirectResponse(url=f'/bundles/{bundle_id}', status_code=303)
