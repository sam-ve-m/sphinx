from fastapi import Request, Depends, UploadFile, File
from typing import Union

from src.controllers.base_controller import BaseController
from src.controllers.terms.controller import TermsController
from src.domain.validators.onboarding_validators import TermFile
from src.routers.routes_registers.admin import AdminRouter


router = AdminRouter.instance()


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
        {
            "file_or_base64": file_or_base64,
        }
    )
    return BaseController.run(TermsController.save_term, payload, request)
