from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Login(BaseModel):
    email: str


@router.post("/login", tags=["authenticate"])
async def login(login: Login):
    return 200


@router.post("/login/admin", tags=["authenticate"])
async def login_admin(login: Login):
    return 200


@router.get("/thebes_gate/{token}", tags=["authenticate"])
async def answer(token: str):
    return 200
