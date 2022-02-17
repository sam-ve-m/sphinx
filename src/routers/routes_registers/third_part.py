from starlette.requests import Request
import logging

# Sphinx
from src.core.abstract_classes.routes_register.register import RoutesRegister
from src.routers.routes_registers.middleware_functions import MiddlewareUtils
from src.infrastructures.env_config import config


class ThirdPartRouter(RoutesRegister):

    _instance = None

    @staticmethod
    async def is_allow(request: Request, middleware_utils=MiddlewareUtils) -> bool:
        try:
            token = middleware_utils.get_token_if_token_is_valid(request=request)
            if token and token.get("is_third_part"):
                return True
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
        return False
