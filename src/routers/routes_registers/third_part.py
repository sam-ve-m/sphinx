from starlette.requests import Request

# Sphinx
from src.core.abstract_classes.routes_register.register import RoutesRegister


class ThirdPartRouter(RoutesRegister):

    _instance = None

    @staticmethod
    def is_allow(request: Request) -> bool:
        print('ThirdPartRouter')
        return True
