# OUTSIDE LIBRARIES
import os
from typing import List

# STANDARD LIBS
from contextlib import contextmanager
import logging

# OUTSIDE LIBRARIES
import cx_Oracle
from decouple import config

# SPHINX
from src.interfaces.repositories.oracle.interface import IOracle

cx_Oracle.init_oracle_client(lib_dir=config("ORACLE_LD_LIBRARY_PATH"))


class OracleInfrastructure(IOracle):

    pool = cx_Oracle.SessionPool(
        user=config("ORACLE_USER"),
        password=config("ORACLE_PASSWORD"),
        min=1,
        max=100,
        increment=1,
        dsn=cx_Oracle.makedsn(
            config("ORACLE_BASE_DSN"),
            config("ORACLE_PORT"),
            service_name=config("ORACLE_SERVICE"),
        ),
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
                rows = cursor.fetchall()
                rows = self._normalize_encode(rows=rows)
                return rows

    @staticmethod
    def _normalize_encode(rows: List[tuple]) -> List[tuple]:
        new_rows = list()
        for row in rows:
            new_row = list()
            for item in row:
                if type(item) == str:
                    item = item.encode().decode("utf-8", "strict")
                new_row.append(item)
            new_rows.append(tuple(new_row))
        return new_rows

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
