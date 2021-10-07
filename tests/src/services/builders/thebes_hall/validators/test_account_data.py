# STANDARD LIBS
from datetime import datetime
from freezegun import freeze_time

# Sphinx
from src.services.builders.thebes_hall.validators.account_data import AccountData


def test_run_without_last_modified_date():
    user_data = {}
    AccountData.run(user_data=user_data)
    assert user_data == {}


def test_run_without_concluded_at():
    user_data = {
        "last_modified_date": {}
    }
    AccountData.run(user_data=user_data)
    assert user_data["last_modified_date"].get('months_past') is None


@freeze_time("2022-04-01")
def test_run():
    user_data = {
        "last_modified_date": {
            "concluded_at": datetime(
                year=2021,
                month=1,
                day=1,
                hour=1,
                minute=1,
                second=1,
                microsecond=1
            )
        }
    }
    AccountData.run(user_data=user_data)
    assert user_data["last_modified_date"]["months_past"] == 15
