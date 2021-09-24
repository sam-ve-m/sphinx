# OUTSIDE LIBRARIES
from src.utils.env_config import config

# SPHINX
from src.core.interfaces.services.builders.thebes_hall.validators.interface import (
    IValidator,
)
from src.repositories.file.repository import FileRepository


class Terms(IValidator):
    @staticmethod
    def run(payload: dict) -> dict:
        file_repository = FileRepository(config("AWS_BUCKET_TERMS"))
        terms_version = file_repository.get_terms_version()
        user_terms = payload.get("terms")
        if user_terms:
            for user_term, values in user_terms.items():
                if values and values.get("version") < terms_version.get(user_term):
                    values["is_deprecated"] = True
        return payload
