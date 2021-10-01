# Standards
from abc import ABC, abstractmethod
from typing import Callable
from starlette.requests import Request
from starlette.routing import Match
from starlette.middleware.base import BaseHTTPMiddleware
import json

# Third Part
from fastapi import APIRouter, FastAPI, status, Response

# Sphinx
from src.i18n.i18n_resolver import i18nResolver as i18n
from src.routers.routes_registers.middleware_functions import MiddlewareUtils


class RoutesRegister(ABC):
    def __init__(self):
        raise Exception("You are using Sphinx ways (routers) wrong!")

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = APIRouter()
        return cls._instance

    @classmethod
    def apply_middleware(cls, app):
        if cls._instance is None:
            raise Exception(
                """
                    You did not have initialize this route, 
                    try again when you initialize this instance. The gods are watching you.
                """
            )
        router = cls._instance

        @cls.router_middleware(app, router)
        async def middleware(request: Request, call_next):
            if cls.is_allow(request):
                response = await call_next(request)
                return response
            return RoutesRegister.get_unauthorized_response(request=request)

    @staticmethod
    def router_middleware(app: FastAPI, router: APIRouter):
        """Decorator to add a router-specific middleware."""

        def deco(func: Callable) -> Callable:
            async def _middleware(request: Request, call_next):
                # Check if scopes match
                matches = any(
                    [
                        route.matches(request.scope)[0] == Match.FULL
                        for route in router.routes
                    ]
                )
                if matches:  # Run the middleware if they do
                    return await func(request, call_next)
                else:  # Otherwise skip the middleware
                    return await call_next(request)

            app.add_middleware(BaseHTTPMiddleware, dispatch=_middleware)
            return func

        return deco

    @staticmethod
    def get_unauthorized_response(request: Request):
        locale = i18n.get_language_from_request(request=request)
        status_code = status.HTTP_401_UNAUTHORIZED
        content = {
            "detail": [
                {
                    "msg": i18n.get_translate(
                        "invalid_credential",
                        locale=locale,
                    )
                }
            ]
        }
        return Response(content=json.dumps(content), status_code=status_code)

    @staticmethod
    @abstractmethod
    def is_allow(request: Request, middleware_utils=MiddlewareUtils) -> bool:
        pass
