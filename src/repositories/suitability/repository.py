# OUTSIDE LIBRARIES
from src.infrastructures.env_config import config

# SPHINX
from src.repositories.base_repository.mongo_db.base import MongoDbBaseRepository


class SuitabilityRepository(MongoDbBaseRepository):
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_SUITABILITY_COLLECTION")


class SuitabilityUserProfileRepository(MongoDbBaseRepository):
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_SUITABILITY_USER_PROFILE_COLLECTION")


class SuitabilityAnswersRepository(MongoDbBaseRepository):
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_SUITABILITY_ANSWERS_COLLECTION")
