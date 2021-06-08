# SPHINX
from src.services.builders.thebes_hall.validators.terms import Terms as TermsValidator
from src.services.builders.thebes_hall.validators.suitability import (
    Suitability as SuitabilityValidator,
)
from src.services.builders.thebes_hall.validators.account_data import (
    AccountData as AccountDataValidator,
)


class ThebesHall:

    validators = [TermsValidator, SuitabilityValidator, AccountDataValidator]

    @staticmethod
    def validate(payload: dict) -> dict:
        for validator in ThebesHall.validators:
            validator.run(payload=payload)
        return payload
