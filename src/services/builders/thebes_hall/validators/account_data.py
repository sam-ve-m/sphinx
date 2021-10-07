# STANDARD LIBS
from datetime import datetime

# SPHINX
from src.core.interfaces.services.builders.thebes_hall.validators.interface import (
    IValidator,
)
from src.services.builders.thebes_hall.validators.months_past import months_past


class AccountData(IValidator):
    @staticmethod
    def run(user_data: dict) -> dict:
        if last_modified_date := user_data.get("last_modified_date"):
            if concluded_at := last_modified_date.get("concluded_at"):
                total_months_past = months_past(date=concluded_at)
                last_modified_date["months_past"] = total_months_past
        return user_data
