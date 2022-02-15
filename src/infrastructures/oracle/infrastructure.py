# OUTSIDE LIBRARIES
from typing import List

# STANDARD LIBS
from contextlib import asynccontextmanager
import logging

# OUTSIDE LIBRARIES
import cx_Oracle_async

# SPHINX
from src.infrastructures.env_config import config


class OracleInfrastructure:

    pool = None

    @classmethod
    async def _get_pool(cls):
        if cls.pool is None:
            cls.pool = await cx_Oracle_async.SessionPool(
                user=config("ORACLE_USER"),
                password=config("ORACLE_PASSWORD"),
                min=2,
                max=100,
                increment=1,
                dsn=await cx_Oracle_async.makedsn(
                    config("ORACLE_BASE_DSN"),
                    config("ORACLE_PORT"),
                    service_name=config("ORACLE_SERVICE"),
                ),
                encoding=config("ORACLE_ENCODING"),
                getmode=await cx_Oracle_async.SPOOL_ATTRVAL_WAIT,
            )
        return cls.pool

    @asynccontextmanager
    async def get_connection(self):
        pool = await OracleInfrastructure._get_pool()
        connection = pool.acquire()
        yield connection
        pool.release(connection)
