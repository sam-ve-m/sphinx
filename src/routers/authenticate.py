from fastapi import APIRouter

router = APIRouter()


@router.post("/login", tags=["authenticate"])
async def login():
    return 200


@router.post("/login/admin", tags=["authenticate"])
async def login_admin():
    return 200

