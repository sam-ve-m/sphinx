from starlette.requests import Request
from etria_logger import Gladsheim

# Sphinx
from src.core.abstract_classes.routes_register.register import RoutesRegister
from src.services.middleware.service import MiddlewareService


class UnvalidatedUserRouter(RoutesRegister):

    _instance = None

    @staticmethod
    async def is_allow(request: Request, middleware_utils=MiddlewareService) -> bool:
        allowed_user = False
        try:
            if token := await middleware_utils.get_token_if_token_is_valid(
                request=request
            ):
                allowed_user = True
        except Exception as e:
            Gladsheim.error(error=e)
        return allowed_user
