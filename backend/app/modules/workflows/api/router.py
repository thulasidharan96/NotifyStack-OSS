from fastapi import APIRouter

router = APIRouter(prefix="/workflows", tags=["workflows"])


@router.get("")
async def list_workflows() -> dict[str, list[str]]:
    return {"workflows": []}
