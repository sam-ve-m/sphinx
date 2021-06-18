from fastapi import APIRouter, Request, Depends, UploadFile, File, Form
from typing import Union

from src.controllers.base_controller import BaseController
from src.controllers.terms.controller import TermsController
from src.routers.validators.base import TermFile


router = APIRouter()


@router.post("/term", tags=["term"], include_in_schema=False)
async def save_term(
    request: Request,
    file_type: TermFile = Depends(TermFile.as_form),
    file_or_base64: Union[UploadFile, str] = File(...),
):
    if isinstance(file_or_base64, str) is False:
        file_or_base64 = await file_or_base64.read()
    payload = file_type.dict()
    payload.update(
        {"file_or_base64": file_or_base64,}
    )
    return BaseController.run(TermsController.save_term, payload, request)


@router.get("/term", tags=["term"])
async def get_term_file(request: Request, file_type: TermFile = Depends(TermFile)):
    return BaseController.run(TermsController.get_term, file_type.dict(), request)
