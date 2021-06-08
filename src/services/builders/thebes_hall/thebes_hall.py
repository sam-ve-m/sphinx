# SPHINX
from src.services.builders.thebes_hall.validators.terms import Terms as TermsValidator


class ThebesHall:

    validators = [
        TermsValidator,
    ]

    @staticmethod
    def validate(payload: dict) -> dict:
        for validator in ThebesHall.validators:
            validator.run(payload=payload)
        return payload
