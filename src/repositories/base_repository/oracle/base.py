# OUTSIDE LIBRARIES
from typing import List

# STANDARD LIBS
import logging

# OUTSIDE LIBRARIES
import cx_Oracle

# SPHINX
from src.exceptions.exceptions import InternalServerError
from src.core.interfaces.repositories.oracle.interface import IOracle
from src.infrastructures.env_config import config
from src.infrastructures.oracle.infrastructure import OracleInfrastructure


class OracleBaseRepository(OracleInfrastructure, IOracle):
    async def query(self, sql: str) -> list:
        try:
            async with self.get_connection() as connection:
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
            raise InternalServerError("common.process_issue")

        except cx_Oracle.ProgrammingError as e:
            (error,) = e.args
            logger = logging.getLogger(config("LOG_NAME"))
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Sql: {sql} - Oracle-ex: {e}"
            logger.error(message, exc_info=True)
            raise InternalServerError("common.process_issue")

        except cx_Oracle.InternalError as e:
            (error,) = e.args
            logger = logging.getLogger(config("LOG_NAME"))
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Sql: {sql} - Oracle-ex: {e}"
            logger.error(message, exc_info=True)
            raise InternalServerError("common.process_issue")

        except cx_Oracle.NotSupportedError as e:
            (error,) = e.args
            logger = logging.getLogger(config("LOG_NAME"))
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Sql: {sql} - Oracle-ex: {e}"
            logger.error(message, exc_info=True)
            raise InternalServerError("common.process_issue")

        except cx_Oracle.DatabaseError as e:
            (error,) = e.args
            logger = logging.getLogger(config("LOG_NAME"))
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Sql: {sql} - Oracle-ex: {e}"
            logger.error(message, exc_info=True)
            raise InternalServerError("common.process_issue")

        except cx_Oracle.Error as e:
            (error,) = e.args
            logger = logging.getLogger(config("LOG_NAME"))
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Sql: {sql} - Oracle-ex: {e}"
            logger.error(message, exc_info=True)
            raise InternalServerError("common.process_issue")

        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            message = f"Exception: {e}. Oracle-Error-Base-Exception Sql: {sql}"
            logger.error(message, exc_info=True)
            raise InternalServerError("common.process_issue")

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
            raise InternalServerError("common.process_issue")

        except cx_Oracle.ProgrammingError as e:
            (error,) = e.args
            logger = logging.getLogger(config("LOG_NAME"))
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Values: {values} - Oracle-ex: {e}"
            logger.error(message, exc_info=True)
            raise InternalServerError("common.process_issue")

        except cx_Oracle.InternalError as e:
            (error,) = e.args
            logger = logging.getLogger(config("LOG_NAME"))
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Values: {values} - Oracle-ex: {e}"
            logger.error(message, exc_info=True)
            raise InternalServerError("common.process_issue")

        except cx_Oracle.NotSupportedError as e:
            (error,) = e.args
            logger = logging.getLogger(config("LOG_NAME"))
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Values: {values} - Oracle-ex: {e}"
            logger.error(message, exc_info=True)
            raise InternalServerError("common.process_issue")

        except cx_Oracle.DatabaseError as e:
            (error,) = e.args
            logger = logging.getLogger(config("LOG_NAME"))
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Values: {values} - Oracle-ex: {e}"
            logger.error(message, exc_info=True)
            raise InternalServerError("common.process_issue")

        except cx_Oracle.Error as e:
            (error,) = e.args
            logger = logging.getLogger(config("LOG_NAME"))
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Values: {values} - Oracle-ex: {e}"
            logger.error(message, exc_info=True)
            raise InternalServerError("common.process_issue")
