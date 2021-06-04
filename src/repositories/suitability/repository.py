from src.repositories.base_repository import BaseRepository
from decouple import config


class SuitabilityRepository(BaseRepository):
    def __init__(self):
        super().__init__(
            database=config("MONGODB_DATABASE_NAME"),
            collection=config("MONGODB_SUITABILITY_COLLECTION"),
        )
