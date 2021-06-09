# STANDARD LIBS
from datetime import datetime

# SPHINX
from src.interfaces.services.builders.thebes_hall.validators.interface import IValidator


class Suitability(IValidator):
    @staticmethod
    def run(payload: dict) -> dict:
        suitability = payload.get("suitability")
        if suitability:
            submission_date = suitability.get("submission_date")
            months_past = Suitability.months_past(submission_date=submission_date)
            suitability["months_past"] = months_past
        return payload

    @staticmethod
    def months_past(submission_date: datetime):
        nowadays = datetime.strptime(
            datetime.strftime(datetime.now(), "%Y-%m-%d"), "%Y-%m-%d"
        )
        num_months = (nowadays.year - submission_date.year) * 12 + (
            nowadays.month - submission_date.month
        )
        return num_months
