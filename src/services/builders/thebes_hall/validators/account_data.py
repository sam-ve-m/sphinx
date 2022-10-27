# STANDARD LIBS

# SPHINX
from src.core.interfaces.services.builders.thebes_hall.validators.interface import (
    IValidator,
)
from src.services.builders.thebes_hall.validators.months_past import months_past


class AccountData(IValidator):
    @staticmethod
    def run(user_data: dict) -> dict:
        if record_date_control := user_data.get("record_date_control"):
            if registry_updates := record_date_control.get("registry_updates"):
                if last_registration_data_update := registry_updates.get(
                    "last_registration_data_update"
                ):
                    total_months_past = months_past(date=last_registration_data_update)
                    registry_updates["months_past"] = total_months_past
        return user_data
