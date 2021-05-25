from fastapi import APIRouter

router = APIRouter()


@router.get("/pendencies", tags=["pendencies"])
async def pendencies():
    return 200
