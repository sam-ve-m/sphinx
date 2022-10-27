# STANDARD LIBS

# SPHINX
from src.core.interfaces.services.builders.thebes_hall.validators.interface import (
    IValidator,
)
from src.services.builders.thebes_hall.validators.months_past import months_past


class Suitability(IValidator):
    @staticmethod
    def run(user_data: dict) -> dict:
        if suitability := user_data.get("suitability"):
            total_months_past = months_past(date=suitability["submission_date"])
            user_data["suitability"]["months_past"] = total_months_past
            user_data["suitability"]["remaining_months"] = 24 - total_months_past
        return user_data
