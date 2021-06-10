# STANDARD LIBS
from datetime import datetime

# SPHINX
from src.interfaces.services.builders.thebes_hall.validators.interface import IValidator


class AccountData(IValidator):
    @staticmethod
    def run(payload: dict) -> dict:
        provided_by_bureaux = payload.get("provided_by_bureaux")
        if provided_by_bureaux:
            concluded_at = provided_by_bureaux.get("concluded_at")
            if concluded_at:
                months_past = AccountData.months_past(concluded_at=concluded_at)
                provided_by_bureaux["months_past"] = months_past
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
