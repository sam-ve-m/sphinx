from src.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):

    def __init__(self):
        super.__init__(database='sphinx', collection='users')
