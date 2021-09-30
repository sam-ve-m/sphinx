from starlette.requests import Request

# Sphinx
from src.core.abstract_classes.routes_register.register import RoutesRegister
from src.utils.middleware import MiddlewareUtils


class ClientRouter(RoutesRegister):

    _instance = None

    @staticmethod
    def is_allow(request: Request, middleware_utils=MiddlewareUtils) -> bool:
        allowed_client = False
        if token := middleware_utils.get_token_if_token_is_valid(request=request):
            if valid_client := middleware_utils.get_valid_user_from_database(token=token):
                if middleware_utils.is_user_token_life_time_valid(user_data=valid_client, token=token):
                    allowed_client = middleware_utils.validate_electronic_signature(
                        request=request, user_data=valid_client
                    )
        return allowed_client
