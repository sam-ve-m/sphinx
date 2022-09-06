# OUTSIDE LIBRARIES
from fastapi import Request, Depends

# SPHINX
from src.domain.validators.onboarding_validators import (
    TermFile,
    TermsFile,
)
from src.routers.routes_registers.unvalidated_user import UnvalidatedUserRouter
from src.services.jwts.service import JwtService
from src.controllers.base_controller import BaseController
from src.controllers.users.controller import UserController

router = UnvalidatedUserRouter.instance()


@router.put("/user/sign_terms", tags=["user"])
async def sign_term(
    request: Request,
    file_types: TermsFile,
):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)

    payload = file_types.dict()
    payload.update({"x-thebes-answer": jwt_data})
    return await BaseController.run(UserController.sign_terms, payload, request)


@router.get("/user/signed_term", tags=["user"])
async def get_assigned_term(
    request: Request,
    file_type: TermFile = Depends(TermFile),
):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    payload = file_type.dict()
    payload.update({"x-thebes-answer": jwt_data})
    return await BaseController.run(UserController.get_signed_term, payload, request)
