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

    @staticmethod
    def start_oracle():
        OracleInfrastructure.pool = cx_Oracle.SessionPool(
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

    @contextmanager
    def get_connection(self):
        if OracleInfrastructure.pool is None:
            OracleInfrastructure.start_oracle()
        connection = self.pool.acquire()
        try:
            yield connection
        except (cx_Oracle.Error, Exception) as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
        finally:
            self.pool.release(connection)
