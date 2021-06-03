from fastapi import APIRouter, Request, Form, UploadFile, File
from typing import Union

from src.controllers.base_controller import BaseController
from src.controllers.terms.controller import TermsController
from src.routers.validators.base import FileType


router = APIRouter()


@router.post("/term", tags=["term"])
async def save_user_self(
    request: Request,
    file_type: str = Form(...),
    file_or_base64: Union[UploadFile, str] = File(...),
):
    if isinstance(file_or_base64, str) is False:
        file_or_base64 = await file_or_base64.read()
    payload = {
        "file_type": file_type,
        "file_or_base64": file_or_base64,
    }
    return BaseController.run(TermsController.save_term, payload, request)
