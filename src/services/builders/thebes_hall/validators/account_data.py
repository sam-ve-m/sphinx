# STANDARD LIBS
from datetime import datetime

# SPHINX
from src.core.interfaces.services.builders.thebes_hall.validators.interface import (
    IValidator,
)


class AccountData(IValidator):
    @staticmethod
    def run(user_data: dict) -> dict:
        last_modified_date = user_data.get("last_modified_date")
        if last_modified_date:
            concluded_at = last_modified_date.get("concluded_at")
            if concluded_at:
                months_past = AccountData.months_past(concluded_at=concluded_at)
                last_modified_date["months_past"] = months_past
        return user_data

    @staticmethod
    def months_past(concluded_at: datetime):
        nowadays = datetime.strptime(
            datetime.strftime(datetime.now(), "%Y-%m-%d"), "%Y-%m-%d"
        )
        num_months = (nowadays.year - concluded_at.year) * 12 + (
            nowadays.month - concluded_at.month
        )
        return num_months
