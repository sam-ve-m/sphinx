from starlette.requests import Request

# Sphinx
from src.core.abstract_classes.routes_register.register import RoutesRegister
from src.utils.middleware import MiddlewareUtils


class PublicRouter(RoutesRegister):

    _instance = None

    @staticmethod
    def is_allow(request: Request, middleware_utils=MiddlewareUtils) -> bool:
        return True
