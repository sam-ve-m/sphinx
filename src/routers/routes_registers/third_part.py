from starlette.requests import Request
from etria_logger import Gladsheim

# Sphinx
from src.core.abstract_classes.routes_register.register import RoutesRegister
from src.services.middleware.service import MiddlewareService


class ThirdPartRouter(RoutesRegister):

    _instance = None

    @staticmethod
    async def is_allow(request: Request, middleware_utils=MiddlewareService) -> bool:
        try:
            token = await middleware_utils.get_token_if_token_is_valid(request=request)
            if token and token.get("is_third_part"):
                return True
        except Exception as e:
            Gladsheim.error(error=e)
        return False
