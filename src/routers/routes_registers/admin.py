from starlette.requests import Request
from etria_logger import Gladsheim

# Sphinx
from src.core.abstract_classes.routes_register.register import RoutesRegister
from src.routers.routes_registers.middleware_functions import MiddlewareUtils


class AdminRouter(RoutesRegister):

    _instance = None

    @staticmethod
    async def is_allow(request: Request, middleware_utils=MiddlewareUtils) -> bool:
        return True
        allowed_admin = False
        try:
            if token := await middleware_utils.get_token_if_token_is_valid(
                request=request
            ):
                if valid_admin := await middleware_utils.get_valid_admin_from_database(
                    token=token
                ):
                    allowed_admin = middleware_utils.is_user_token_life_time_valid(
                        user_data=valid_admin, token=token
                    )
        except Exception as e:
            Gladsheim.error(error=e)
        return allowed_admin
