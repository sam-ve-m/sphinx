from typing import Optional


class StubbyBaseRepository:

    def __init__(self, database: str, collection: str) -> None:
        self.database = database
        self.collection = collection

    def insert(self, data: dict) -> bool:
        pass

    def insert_many(self, data: list) -> bool:
        pass

    def find_one(self, query: dict) -> Optional[dict]:
        return dict

    def find_more_than_equal_one(self, query: dict) -> Optional[list]:
        return list

    def find_all(self) -> Optional[list]:
        return list

    def update_one(self, old: dict, new: dict) -> bool:
        pass

    def delete_one(self, entity: dict) -> bool:
        pass
