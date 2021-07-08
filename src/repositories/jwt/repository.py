# OUTSIDE LIBRARIES
from src.utils.env_config import config

# SPHINX
from src.repositories.base_repository import BaseRepository


class JwtRepository(BaseRepository):
    def __init__(self):
        super().__init__(
            database=config("MONGODB_DATABASE_NAME"),
            collection=config("MONGODB_JWT_COLLECTION"),
        )
