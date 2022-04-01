# Third part
from datetime import datetime

# Sphinx
import pytest
from freezegun import freeze_time

from src.services.builders.thebes_hall.validators.suitability import Suitability


def test_run_without_suitability():
    user_data = {}
    Suitability.run(user_data)
    assert user_data == {}


def test_run_without_submission_date_in_suitability():
    user_data = {"suitability": {"fake_key": None}}
    with pytest.raises(KeyError):
        Suitability.run(user_data)


@freeze_time("2022-04-01")
def test_run_with_empty_terms_version():
    user_data = {
        "suitability": {
            "submission_date": datetime(
                year=2021, month=1, day=1, hour=1, minute=1, second=1, microsecond=1
            )
        }
    }
    Suitability.run(user_data)
    assert user_data["suitability"]["months_past"] == 15
