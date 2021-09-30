from starlette.requests import Request

# Sphinx
from src.core.abstract_classes.routes_register.register import RoutesRegister
from src.utils.middleware import MiddlewareUtils


class UserRouter(RoutesRegister):

    _instance = None

    @staticmethod
    def is_allow(request: Request, middleware_utils=MiddlewareUtils) -> bool:
        allowed_user = False
        if token := middleware_utils.get_token_if_token_is_valid(request=request):
            if valid_user := middleware_utils.get_valid_user_from_database(token=token):
                allowed_user = middleware_utils.is_user_token_life_time_valid(
                    user_data=valid_user, token=token
                )
        return allowed_user
