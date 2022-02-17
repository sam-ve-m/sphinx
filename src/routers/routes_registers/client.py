from starlette.requests import Request
import logging

# Sphinx
from src.core.abstract_classes.routes_register.register import RoutesRegister
from src.routers.routes_registers.middleware_functions import MiddlewareUtils
from src.infrastructures.env_config import config


class ClientRouter(RoutesRegister):

    _instance = None

    @staticmethod
    async def is_allow(request: Request, middleware_utils=MiddlewareUtils) -> bool:
        allowed_client = False
        try:
            if token := middleware_utils.get_token_if_token_is_valid(request=request):
                if valid_client := await middleware_utils.get_valid_user_from_database(
                    token=token
                ):
                    if middleware_utils.is_user_token_life_time_valid(
                        user_data=valid_client, token=token
                    ):
                        allowed_client = middleware_utils.validate_electronic_signature(
                            request=request, user_data=valid_client
                        )
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
        return allowed_client
