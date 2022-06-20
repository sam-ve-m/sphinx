# Third part
from fastapi import Request, status, Response, Depends
from etria_logger import Gladsheim
import json

# Sphinx
from src.controllers.base_controller import BaseController
from src.domain.validators.authenticate_validators import Login
from src.controllers.authentications.controller import AuthenticationController
from src.routers.routes_registers.public import PublicRouter
from src.services.jwts.service import JwtService
from src.i18n.i18n_resolver import i18nResolver as i18n
from src.domain.validators.authenticate_validators import Cpf

router = PublicRouter.instance()


@router.post("/login", tags=["authentication"])
async def login(user_credentials: Login, request: Request):
    return await BaseController.run(
        AuthenticationController.login, dict(user_credentials), request
    )


@router.get("/validate_cpf", tags=["authentication"])
async def login(request: Request, cpf: Cpf = Depends(Cpf)):
    return await BaseController.run(
        AuthenticationController.validate_cpf, cpf.dict()["cpf"], request
    )


@router.get("/thebes_gate", tags=["authentication"])
async def answer(request: Request):
    try:
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    except Exception as e:
        Gladsheim.error(error=e)
        lang = i18n.get_language_from_request(request=request)
        return Response(
            content=json.dumps(
                {
                    "detail": [
                        {"msg": i18n.get_translate("invalid_credential", locale=lang)}
                    ]
                }
            ),
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    return await BaseController.run(
        AuthenticationController.thebes_gate,
        jwt_data,
        request,
    )
