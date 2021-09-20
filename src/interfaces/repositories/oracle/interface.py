# STANDARD LIBS
from abc import ABC, abstractmethod
from contextlib import contextmanager


class IOracle(ABC):

    pool = None

    @contextmanager
    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def query(self, sql) -> list:
        pass

    @abstractmethod
    def execute(self, sql, values) -> None:
        pass
