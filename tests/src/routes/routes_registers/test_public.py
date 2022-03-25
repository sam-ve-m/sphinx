from unittest.mock import MagicMock

# Sphinx
from src.routers.routes_registers.public import PublicRouter
from tests.stub_classes.stub_middleware_utils import StubMiddlewareUtils
from tests.stub_classes.stub_request import StubRequest, StubURL


def test_is_allow():
    middleware_utils = StubMiddlewareUtils()
    middleware_utils.get_token_if_token_is_valid = MagicMock(return_value=None)
    assert PublicRouter.is_allow(StubRequest(StubURL), middleware_utils) is True
