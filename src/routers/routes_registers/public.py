from starlette.requests import Request

# Sphinx
from src.core.abstract_classes.routes_register.register import RoutesRegister
from src.services.middleware.service import MiddlewareService


class PublicRouter(RoutesRegister):

    _instance = None

    @staticmethod
    async def is_allow(request: Request, middleware_utils=MiddlewareService) -> bool:
        return True
