# OUTSIDE LIBRARIES
from src.utils.env_config import config

# SPHINX
from src.repositories.base_repository import BaseRepository


class SuitabilityRepository(BaseRepository):
    def __init__(self):
        super().__init__(
            database=config("MONGODB_DATABASE_NAME"),
            collection=config("MONGODB_SUITABILITY_COLLECTION"),
        )


class SuitabilityUserProfileRepository(BaseRepository):
    def __init__(self):
        super().__init__(
            database=config("MONGODB_DATABASE_NAME"),
            collection=config("MONGODB_SUITABILITY_USER_PROFILE_COLLECTION"),
        )


class SuitabilityAnswersRepository(BaseRepository):
    def __init__(self):
        super().__init__(
            database=config("MONGODB_DATABASE_NAME"),
            collection=config("MONGODB_SUITABILITY_ANSWERS_COLLECTION"),
        )
