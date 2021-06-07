from fastapi import APIRouter

router = APIRouter()


@router.get("/dependency", tags=["dependency"])
def pendencies():
    return 200
