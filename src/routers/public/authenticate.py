# Third part
from fastapi import Request, status, Response
import logging
import json

# Sphinx
from src.infrastructures.env_config import config
from src.controllers.base_controller import BaseController
from src.domain.validators.authenticate_validators import Login
from src.controllers.authentications.controller import AuthenticationController
from src.routers.routes_registers.public import PublicRouter
from src.services.jwts.service import JwtService
from src.i18n.i18n_resolver import i18nResolver as i18n

router = PublicRouter.instance()


@router.post("/login", tags=["authentication"])
def login(user_credentials: Login, request: Request):
    return BaseController.run(
        AuthenticationController.login, dict(user_credentials), request
    )


@router.get("/thebes_gate", tags=["authentication"])
def answer(request: Request):
    try:
        jwt_data = JwtService.get_thebes_answer_from_request(request=request)
    except Exception as e:
        logger = logging.getLogger(config("LOG_NAME"))
        logger.error(e, exc_info=True)
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
    return BaseController.run(
        AuthenticationController.thebes_gate,
        jwt_data,
        request,
    )
