# OUTSIDE LIBRARIES
from src.infrastructures.env_config import config

# SPHINX
from src.infrastructures.mongo_db.infrastructure import MongoDBInfrastructure


class SuitabilityRepository(MongoDBInfrastructure):
    def __init__(self):
        super().__init__(
            database=config("MONGODB_DATABASE_NAME"),
            collection=config("MONGODB_SUITABILITY_COLLECTION"),
        )


class SuitabilityUserProfileRepository(MongoDBInfrastructure):
    def __init__(self):
        super().__init__(
            database=config("MONGODB_DATABASE_NAME"),
            collection=config("MONGODB_SUITABILITY_USER_PROFILE_COLLECTION"),
        )


class SuitabilityAnswersRepository(MongoDBInfrastructure):
    def __init__(self):
        super().__init__(
            database=config("MONGODB_DATABASE_NAME"),
            collection=config("MONGODB_SUITABILITY_ANSWERS_COLLECTION"),
        )
