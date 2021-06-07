
# OUTSIDE LIBRARIES
from decouple import config

# SPHINX
from src.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(
            database=config("MONGODB_DATABASE_NAME"),
            collection=config("MONGODB_USER_COLLECTION"),
        )
