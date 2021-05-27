from fastapi import APIRouter, Request
from pydantic import BaseModel
from src.utils.jwt_utils import JWTHandler
router = APIRouter()


class Login(BaseModel):
    email: str


@router.post("/login", tags=["authenticate"])
async def login(login: Login):
    return 200


@router.post("/login/admin", tags=["authenticate"])
async def login_admin(login: Login):
    return 200


@router.get("/thebes_gate", tags=["authenticate"])
async def answer(request:Request):
    thebes_answer = None
    for header_tuple in request.headers.raw:
        if b'thebes_answer' in header_tuple:
            thebes_answer = header_tuple[1].decode()
            break
    thebes_answer_data = JWTHandler.decrpty_to_paylod(thebes_answer)
    print(thebes_answer_data)
    return 200
