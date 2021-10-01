from starlette.requests import Request

# Sphinx
from src.core.abstract_classes.routes_register.register import RoutesRegister
from src.routers.routes_registers.middleware_functions import MiddlewareUtils


class AdminRouter(RoutesRegister):

    _instance = None

    @staticmethod
    def is_allow(request: Request, middleware_utils=MiddlewareUtils) -> bool:
        allowed_admin = False
        if token := middleware_utils.get_token_if_token_is_valid(request=request):
            if valid_admin := middleware_utils.get_valid_admin_from_database(token=token):
                allowed_admin = middleware_utils.is_user_token_life_time_valid(
                    user_data=valid_admin, token=token
                )
        return allowed_admin
