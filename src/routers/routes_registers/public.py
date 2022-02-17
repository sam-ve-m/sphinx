from starlette.requests import Request

# Sphinx
from src.core.abstract_classes.routes_register.register import RoutesRegister
from src.routers.routes_registers.middleware_functions import MiddlewareUtils


class PublicRouter(RoutesRegister):

    _instance = None

    @staticmethod
    def is_allow(request: Request, middleware_utils=MiddlewareUtils) -> bool:
        return True
