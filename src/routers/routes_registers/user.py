from starlette.requests import Request
import logging

# Sphinx
from src.core.abstract_classes.routes_register.register import RoutesRegister
from src.routers.routes_registers.middleware_functions import MiddlewareUtils
from src.infrastructures.env_config import config


class UserRouter(RoutesRegister):

    _instance = None

    @staticmethod
    async def is_allow(request: Request, middleware_utils=MiddlewareUtils) -> bool:
        allowed_user = False
        try:
            if token := await middleware_utils.get_token_if_token_is_valid(
                request=request
            ):
                if valid_user := await middleware_utils.get_valid_user_from_database(
                    token=token
                ):
                    allowed_user = middleware_utils.is_user_token_life_time_valid(
                        user_data=valid_user, token=token
                    )
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
        return allowed_user
