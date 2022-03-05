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
from src.core.api_router.router import SphinxAPIRouter
from src.i18n.i18n_resolver import i18nResolver as i18n
from src.routers.routes_registers.middleware_functions import MiddlewareUtils


class RoutesRegister(ABC):
    def __init__(self):
        raise Exception("You are using Sphinx ways (routers) wrong!")

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = SphinxAPIRouter()
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
            if await cls.is_allow(request) and await cls.has_permission(request):
                response = await call_next(request)
                return response
            return RoutesRegister.get_unauthorized_response(request=request)

    @staticmethod
    def router_middleware(app: FastAPI, router: APIRouter):
        def deco(func: Callable) -> Callable:
            async def _middleware(request: Request, call_next):
                matches = any(
                    [
                        route.matches(request.scope)[0] == Match.FULL
                        for route in router.routes
                    ]
                )
                if matches:
                    return await func(request, call_next)
                else:
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
    async def is_allow(request: Request, middleware_utils=MiddlewareUtils) -> bool:
        pass

    @classmethod
    async def has_permission(
        cls, request: Request, middleware_utils=MiddlewareUtils
    ) -> bool:
        permissions_mapped = cls._instance.get_permission_by_route(
            route=request.url.path
        )
        if permissions_mapped is None:
            return True
        token = await middleware_utils.get_token_if_token_is_valid(request)
        if token is None:
            return True
        user = await middleware_utils.get_valid_user_from_database(token=token)
        if user is None:
            return False
        scope = user["scope"]
        view_and_feature_permission = list()
        if permissions_mapped["views"]:
            is_view_allowed = scope["view_type"] in permissions_mapped["views"]
            view_and_feature_permission.append(is_view_allowed)
        if permissions_mapped["features"]:
            is_feature_allowed = any(
                [
                    user_view in permissions_mapped["features"]
                    for user_view in scope["features"]
                ]
            )
            view_and_feature_permission.append(is_feature_allowed)
        return all(view_and_feature_permission)
