# OUTSIDE LIBRARIES
from typing import List

# STANDARD LIBS
from contextlib import contextmanager
import logging

# OUTSIDE LIBRARIES
import cx_Oracle

# SPHINX
from src.exceptions.exceptions import InternalServerError
from src.core.interfaces.repositories.oracle import IOracle
from src.utils.env_config import config


class OracleInfrastructure(IOracle):

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

    def query(self, sql: str) -> list:
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    rows = self._normalize_encode(rows=rows)
                    return rows

        except cx_Oracle.DataError as e:
            (error,) = e.args
            logger = logging.getLogger(config("LOG_NAME"))
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Sql: {sql} - Oracle-ex: {e}"
            logger.error(message, exc_info=True)
            raise InternalServerError(message) from e

        except cx_Oracle.ProgrammingError as e:
            (error,) = e.args
            logger = logging.getLogger(config("LOG_NAME"))
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Sql: {sql} - Oracle-ex: {e}"
            logger.error(message, exc_info=True)
            raise InternalServerError(message) from e

        except cx_Oracle.InternalError as e:
            (error,) = e.args
            logger = logging.getLogger(config("LOG_NAME"))
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Sql: {sql} - Oracle-ex: {e}"
            logger.error(message, exc_info=True)
            raise InternalServerError(message) from e

        except cx_Oracle.NotSupportedError as e:
            (error,) = e.args
            logger = logging.getLogger(config("LOG_NAME"))
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Sql: {sql} - Oracle-ex: {e}"
            logger.error(message, exc_info=True)
            raise InternalServerError(message) from e

        except cx_Oracle.DatabaseError as e:
            (error,) = e.args
            logger = logging.getLogger(config("LOG_NAME"))
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Sql: {sql} - Oracle-ex: {e}"
            logger.error(message, exc_info=True)
            raise InternalServerError(message) from e

        except cx_Oracle.Error as e:
            (error,) = e.args
            logger = logging.getLogger(config("LOG_NAME"))
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Sql: {sql} - Oracle-ex: {e}"
            logger.error(message, exc_info=True)
            raise InternalServerError(message) from e

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

    def execute(self, sql, values) -> None:
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(sql, values)
                    connection.commit()

        except cx_Oracle.DataError as e:
            (error,) = e.args
            logger = logging.getLogger(config("LOG_NAME"))
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Values: {values} - Oracle-ex: {e}"
            logger.error(message, exc_info=True)
            raise InternalServerError(message) from e

        except cx_Oracle.ProgrammingError as e:
            (error,) = e.args
            logger = logging.getLogger(config("LOG_NAME"))
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Values: {values} - Oracle-ex: {e}"
            logger.error(message, exc_info=True)
            raise InternalServerError(message) from e

        except cx_Oracle.InternalError as e:
            (error,) = e.args
            logger = logging.getLogger(config("LOG_NAME"))
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Values: {values} - Oracle-ex: {e}"
            logger.error(message, exc_info=True)
            raise InternalServerError(message) from e

        except cx_Oracle.NotSupportedError as e:
            (error,) = e.args
            logger = logging.getLogger(config("LOG_NAME"))
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Values: {values} - Oracle-ex: {e}"
            logger.error(message, exc_info=True)
            raise InternalServerError(message) from e

        except cx_Oracle.DatabaseError as e:
            (error,) = e.args
            logger = logging.getLogger(config("LOG_NAME"))
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Values: {values} - Oracle-ex: {e}"
            logger.error(message, exc_info=True)
            raise InternalServerError(message) from e

        except cx_Oracle.Error as e:
            (error,) = e.args
            logger = logging.getLogger(config("LOG_NAME"))
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Values: {values} - Oracle-ex: {e}"
            logger.error(message, exc_info=True)
            raise InternalServerError(message) from e
