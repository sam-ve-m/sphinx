# OUTSIDE LIBRARIES
from src.infrastructures.env_config import config

# SPHINX
from src.core.interfaces.services.builders.thebes_hall.validators.interface import (
    IValidator,
)
from src.repositories.file.repository import FileRepository


class Terms(IValidator):
    @staticmethod
    def run(
        user_data: dict, file_repository=FileRepository(config("AWS_BUCKET_TERMS"))
    ) -> dict:
        terms_version = file_repository.get_terms_version()
        if user_terms := user_data.get("terms"):
            for user_term, values in user_terms.items():
                if values and values["version"] < terms_version.get(user_term):
                    values["is_deprecated"] = True
        return user_data
