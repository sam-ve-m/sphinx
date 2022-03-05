# Standards
import asyncio

# OUTSIDE LIBRARIES
from src.infrastructures.env_config import config
import nest_asyncio

nest_asyncio.apply()

# SPHINX
from src.core.interfaces.services.builders.thebes_hall.validators.interface import (
    IValidator,
)
from src.repositories.file.repository import FileRepository


class Terms(IValidator):
    @staticmethod
    def run(user_data: dict, file_repository=FileRepository) -> dict:
        current_event_loop = asyncio.get_running_loop()
        task = current_event_loop.create_task(
            file_repository.get_terms_version(bucket_name=config("AWS_BUCKET_TERMS"))
        )
        terms_version = current_event_loop.run_until_complete(task)
        if user_terms := user_data.get("terms"):
            for user_term, values in user_terms.items():
                if values and values["version"] < terms_version.get(user_term):
                    values["is_deprecated"] = True
        return user_data
