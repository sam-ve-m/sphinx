# STANDARD LIBS
from datetime import datetime

# SPHINX
from src.interfaces.services.builders.thebes_hall.validators.interface import IValidator


class AccountData(IValidator):
    @staticmethod
    def run(payload: dict) -> dict:
        user_account_data = payload.get("user_account_data")
        if user_account_data:
            concluded_at = user_account_data.get("concluded_at")
            months_past = AccountData.months_past(
                concluded_at=concluded_at
            )
            user_account_data["months_past"] = months_past
        return payload

    @staticmethod
    def months_past(concluded_at: datetime):
        nowadays = datetime.strptime(
            datetime.strftime(datetime.now(), "%Y-%m-%d"), "%Y-%m-%d"
        )
        num_months = (nowadays.year - concluded_at.year) * 12 + (
            nowadays.month - concluded_at.month
        )
        return num_months
