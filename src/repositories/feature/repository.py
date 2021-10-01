# OUTSIDE LIBRARIES
from src.infrastructures.env_config import config

# SPHINX
from src.infrastructures.mongo_db.infrastructure import MongoDBInfrastructure


class FeatureRepository(MongoDBInfrastructure):
    def __init__(self) -> None:
        super().__init__(
            database=config("MONGODB_DATABASE_NAME"),
            collection=config("MONGODB_FEATURE_COLLECTION"),
        )
