# OUTSIDE LIBRARIES
from typing import List

# STANDARD LIBS
from contextlib import contextmanager
import logging

# OUTSIDE LIBRARIES
import cx_Oracle

# SPHINX
from src.infrastructures.env_config import config


class OracleInfrastructure:

    pool = None

    @classmethod
    def _get_pool(cls):
        if cls.pool is None:
            cls.pool = cx_Oracle.SessionPool(
                user=config("ORACLE_USER"),
                password=config("ORACLE_PASSWORD"),
                min=2,
                max=100,
                increment=1,
                dsn=cx_Oracle.makedsn(
                    config("ORACLE_BASE_DSN"),
                    config("ORACLE_PORT"),
                    service_name=config("ORACLE_SERVICE"),
                ),
                encoding=config("ORACLE_ENCODING"),
                getmode=cx_Oracle.SPOOL_ATTRVAL_WAIT,
            )
        return cls.pool

    @contextmanager
    def get_connection(self):
        pool = OracleInfrastructure._get_pool()
        connection = pool.acquire()
        yield connection
        pool.release(connection)
