# STANDARD LIBS
from contextlib import contextmanager
import logging

# OUTSIDE LIBRARIES
import cx_Oracle
from decouple import config

# SPHINX
from src.interfaces.repositories.oracle.interface import IOracle


class OracleInfrastructure(IOracle):

    pool = cx_Oracle.SessionPool(
        config("ORACLE_USER"),
        config("ORACLE_PASSWORD"),
        config("ORACLE_DATABASE_NAME"),
        min=100,
        max=100,
        increment=0,
        encoding=config("ORACLE_ENCODING"),
    )

    @staticmethod
    @contextmanager
    def get_connection():
        connection = OracleInfrastructure.pool.acquire()
        try:
            yield connection
        except (cx_Oracle.Error, Exception) as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
        finally:
            OracleInfrastructure.pool.release(connection)

    def query(self, sql: str) -> list:
        with OracleInfrastructure.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()

    def insert(self, sql: str, values: list) -> None:
        with OracleInfrastructure.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, values)
                connection.commit()

    def execute(self, name, values) -> int:
        with OracleInfrastructure.get_connection() as connection:
            with connection.cursor() as cursor:
                order_count = cursor.var(int)
                cursor.callproc(name, values)
                return order_count.getvalue()
