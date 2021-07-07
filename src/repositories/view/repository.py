# OUTSIDE LIBRARIES
from decouple import config

# SPHINX
from src.infrastructures.mongo_db.infrastructure import MongoDBInfrastructure


class ViewRepository(MongoDBInfrastructure):
    def __init__(self) -> None:
        super().__init__(
            database=config("MONGODB_DATABASE_NAME"),
            collection=config("MONGODB_VIEW_COLLECTION"),
        )
