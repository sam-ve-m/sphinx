from fastapi import APIRouter

router = APIRouter()


@router.get("/pendencies", tags=["pendencies"])
def pendencies():
    return 200
