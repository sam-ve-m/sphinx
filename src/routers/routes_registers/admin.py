from starlette.requests import Request

# Sphinx
from src.core.abstract_classes.routes_register.register import RoutesRegister
from src.utils.middleware import (
    get_token_if_token_is_valid,
    get_valid_admin_from_database,
    is_user_token_life_time_valid,
)


class AdminRouter(RoutesRegister):

    _instance = None

    @staticmethod
    def is_allow(request: Request) -> bool:
        allowed_admin = False
        if token := get_token_if_token_is_valid(request=request):
            if valid_admin := get_valid_admin_from_database(token=token):
                allowed_admin = is_user_token_life_time_valid(
                    user_data=valid_admin, token=token
                )
        return allowed_admin
