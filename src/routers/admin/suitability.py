# STANDARD LIBS

# OUTSIDE LIBRARIES
from fastapi import Request

# SPHINX
from src.services.validators.suitability_validators import Suitability
from src.controllers.suitabilities.controller import SuitabilityController
from src.controllers.base_controller import BaseController
from src.utils.jwt_utils import JWTHandler
from src.routers.routes_registers.admin import AdminRouter

router = AdminRouter.instance()


@router.post("/suitability/quiz", tags=["suitability"])
async def create_quiz_suitability(suitability: Suitability, request: Request):
    jwt_data = JWTHandler.get_thebes_answer_from_request(request=request)

    payload = {
        "x-thebes-answer": jwt_data,
        "suitability": suitability.dict(),
    }

    return BaseController.run(SuitabilityController.create_quiz, payload, request)
