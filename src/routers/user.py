from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class User(BaseModel):
    name: str
    email: str
    pin: int


class ForgotPassword(BaseModel):
    email: str

@router.post("/user", tags=["user"])
async def create_user(user: User):
    return user, 200


@router.post("/user/admin", tags=["user"])
async def create_admin_user():
    return 200


@router.put("/user", tags=["user"])
async def update_user_data():
    return 200


@router.delete("/user", tags=["user"])
async def delete_user():
    return 200


@router.put("/user/password", tags=["user"])
async def change_user_password():
    return 200


@router.get("/user/forgot_password", tags=["user"])
async def change_user_forgot_password(forgot_password: ForgotPassword):
    return 200


@router.put("/user/view", tags=["user"])
async def change_user_view():
    return 200
