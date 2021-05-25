from fastapi import APIRouter

router = APIRouter()


@router.get("/authorization", tags=["authorization"])
async def user_authorization():
    return 200
