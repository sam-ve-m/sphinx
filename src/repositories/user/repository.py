# OUTSIDE LIBRARIES
from decouple import config

# SPHINX
from src.infrastructures.mongo_db.infrastructure import MongoDBInfrastructure


class UserRepository(MongoDBInfrastructure):
    def __init__(self):
        super().__init__(
            database=config("MONGODB_DATABASE_NAME"),
            collection=config("MONGODB_USER_COLLECTION"),
        )
