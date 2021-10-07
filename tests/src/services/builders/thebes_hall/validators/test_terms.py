# Third part
from unittest.mock import MagicMock

# Sphinx
import pytest

from src.services.builders.thebes_hall.validators.terms import Terms


class StubFileRepository:
    pass


def test_run_without_terms():
    user_data = {}
    stub_file_repository = StubFileRepository()
    stub_file_repository.get_terms_version = MagicMock(return_value={
        "term_of_test": 10
    })
    Terms.run(user_data, file_repository=stub_file_repository)
    assert user_data == {}


def test_run_with_empty_list():
    user_data = {
        "terms": {}
    }
    stub_file_repository = StubFileRepository()
    stub_file_repository.get_terms_version = MagicMock(return_value={
        "term_of_test": 10
    })
    Terms.run(user_data, file_repository=stub_file_repository)
    assert user_data == {
        "terms": {}
    }


def test_run_with_empty_terms_version():
    user_data = {
        "terms": {
            "test_of_terms": {
                "version": 3
            }
        }
    }
    stub_file_repository = StubFileRepository()
    stub_file_repository.get_terms_version = MagicMock(return_value={})
    with pytest.raises(TypeError):
        Terms.run(user_data, file_repository=stub_file_repository)


def test_run_is_deprecated():
    user_data = {
        "terms": {
            "test_of_terms": {
                "version": 3
            }
        }
    }
    stub_file_repository = StubFileRepository()
    stub_file_repository.get_terms_version = MagicMock(return_value={
        "test_of_terms": 4
    })
    Terms.run(user_data, file_repository=stub_file_repository)
    assert user_data == {
        "terms": {
            "test_of_terms": {
                "version": 3,
                "is_deprecated": True
            }
        }
    }


def test_run_is_not_deprecated():
    user_data = {
        "terms": {
            "test_of_terms": {
                "version": 4
            }
        }
    }
    stub_file_repository = StubFileRepository()
    stub_file_repository.get_terms_version = MagicMock(return_value={
        "test_of_terms": 4
    })
    Terms.run(user_data, file_repository=stub_file_repository)
    assert user_data == {
        "terms": {
            "test_of_terms": {
                "version": 4
            }
        }
    }