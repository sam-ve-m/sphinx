# STANDARD LIBS
from abc import ABC, abstractmethod
from contextlib import contextmanager


class IOracle(ABC):

    pool = None

    @abstractmethod
    def query(self, sql) -> list:
        pass

    @abstractmethod
    def execute(self, sql, values) -> None:
        pass
