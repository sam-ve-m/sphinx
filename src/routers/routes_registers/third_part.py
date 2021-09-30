from starlette.requests import Request

# Sphinx
from src.core.abstract_classes.routes_register.register import RoutesRegister
from src.utils.middleware import MiddlewareUtils


class ThirdPartRouter(RoutesRegister):

    _instance = None

    @staticmethod
    def is_allow(request: Request, middleware_utils=MiddlewareUtils) -> bool:
        token = middleware_utils.get_token_if_token_is_valid(request=request)
        if token and token.get("is_third_part"):
            return True
        return False
