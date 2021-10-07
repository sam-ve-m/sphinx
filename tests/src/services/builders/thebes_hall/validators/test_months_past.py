# Third part
from datetime import datetime
from freezegun import freeze_time
import pytest

# Sphinx
from src.services.builders.thebes_hall.validators.months_past import months_past


def test_months_past_wrong_type():
    with pytest.raises(TypeError, match='submission_date is not a datetime'):
        months_past(date={})


@freeze_time("2022-01-01")
def test_months_past_wrong_type():
    ref_datetime = datetime(
        year=2021,
        month=1,
        day=1,
        hour=1,
        minute=1,
        second=1,
        microsecond=1
    )
    total_months_past = months_past(date=ref_datetime)
    assert total_months_past == 12
