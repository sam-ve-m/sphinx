# OUTSIDE LIBRARIES
from src.utils.env_config import config

# SPHINX
from src.repositories.base_repository import BaseRepository


class ViewRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(
            database=config("MONGODB_DATABASE_NAME"),
            collection=config("MONGODB_VIEW_COLLECTION"),
        )
