from fastapi import APIRouter

router = APIRouter(
    prefix='/bundles',
    tags=['Bundles'],
)


@router.get('')
async def get_all_bundles():
    ...
