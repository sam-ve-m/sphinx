# STANDARD LIBS
from abc import ABC, abstractmethod
from contextlib import contextmanager


class IOracle(ABC):

    pool = None

    @staticmethod
    @contextmanager
    @abstractmethod
    def get_connection():
        pass

    @abstractmethod
    def query(self, sql):
        pass

    @abstractmethod
    def insert(self, sql, values):
        pass

    @abstractmethod
    def execute(self, name, values):
        pass
