from starlette.requests import Request
from etria_logger import Gladsheim

# Sphinx
from src.core.abstract_classes.routes_register.register import RoutesRegister
from src.services.middleware.service import MiddlewareService


class ValidatedUserRouter(RoutesRegister):

    _instance = None

    @staticmethod
    async def is_allow(request: Request, middleware_utils=MiddlewareService) -> bool:
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
            Gladsheim.error(error=e)
        return allowed_user
