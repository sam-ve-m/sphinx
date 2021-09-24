from fastapi import Request, Depends

from src.controllers.base_controller import BaseController
from src.controllers.terms.controller import TermsController
from src.routers.validators.base import TermFile
from src.routers.router_registers.public import PublicRouter


router = PublicRouter.instance()


@router.get("/term", tags=["term"])
async def get_term_file(request: Request, file_type: TermFile = Depends(TermFile)):
    return BaseController.run(TermsController.get_term, file_type.dict(), request)


@router.get("/terms", tags=["terms"])
async def get_term_file(request: Request):
    return BaseController.run(TermsController.get_terms, {}, request)
