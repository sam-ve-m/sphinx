from unittest.mock import MagicMock

# Sphinx
from src.routers.routes_registers.user import UserRouter
from tests.stub_classes.stub_middleware_utils import StubMiddlewareUtils
from tests.stub_classes.stub_request import StubRequest, StubURL


def test_is_allow_with_invalid_token():
    middleware_utils = StubMiddlewareUtils()
    middleware_utils.get_token_if_token_is_valid = MagicMock(return_value=None)
    assert UserRouter.is_allow(StubRequest(StubURL), middleware_utils) is False


def test_is_allow_with_invalid_user():
    middleware_utils = StubMiddlewareUtils()
    middleware_utils.get_token_if_token_is_valid = MagicMock(return_value={"a": 1})
    middleware_utils.get_valid_user_from_database = MagicMock(return_value=None)
    assert UserRouter.is_allow(StubRequest(StubURL), middleware_utils) is False


def test_is_allow_with_user_token_life_time_invalid():
    middleware_utils = StubMiddlewareUtils()
    middleware_utils.get_token_if_token_is_valid = MagicMock(return_value={"a": 1})
    middleware_utils.get_valid_user_from_database = MagicMock(return_value={"a": 1})
    middleware_utils.is_user_token_life_time_valid = MagicMock(return_value=False)
    assert UserRouter.is_allow(StubRequest(StubURL), middleware_utils) is False


def test_is_allow_with_user_token_life_time_valid():
    middleware_utils = StubMiddlewareUtils()
    middleware_utils.get_token_if_token_is_valid = MagicMock(return_value={"a": 1})
    middleware_utils.get_valid_user_from_database = MagicMock(return_value={"a": 1})
    middleware_utils.is_user_token_life_time_valid = MagicMock(return_value=True)
    assert UserRouter.is_allow(StubRequest(StubURL), middleware_utils) is True
