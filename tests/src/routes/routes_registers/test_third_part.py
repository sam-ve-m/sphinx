import pytest
from unittest.mock import MagicMock

# Sphinx
from src.routers.routes_registers.third_part import ThirdPartRouter
from tests.stub_classes.stub_request import StubRequest, StubURL
from tests.stub_classes.stub_middleware_utils import StubMiddlewareUtils


def test_is_allow_with_invalid_token():
    middleware_utils = StubMiddlewareUtils()
    middleware_utils.get_token_if_token_is_valid = MagicMock(return_value=None)
    assert ThirdPartRouter.is_allow(StubRequest(StubURL), middleware_utils) is False


def test_is_allow_with_out_is_third_part():
    middleware_utils = StubMiddlewareUtils()
    middleware_utils.get_token_if_token_is_valid = MagicMock(return_value={"a": True})
    assert ThirdPartRouter.is_allow(StubRequest(StubURL), middleware_utils) is False


def test_is_allow():
    middleware_utils = StubMiddlewareUtils()
    middleware_utils.get_token_if_token_is_valid = MagicMock(
        return_value={"is_third_part": True}
    )
    assert ThirdPartRouter.is_allow(StubRequest(StubURL), middleware_utils) is True
