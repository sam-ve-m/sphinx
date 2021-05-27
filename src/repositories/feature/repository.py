from src.repositories.base_repository import BaseRepository
from decouple import config


class FeatureRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(
            database=config("MONGODB_DATABASE_NAME"),
            collection=config("MONGODB_FEATURE_COLLECTION"),
        )
