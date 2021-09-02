# STANDARD LIBS
from typing import Optional
import logging
import json

# OUTSIDE LIBRARIES
from fastapi import Response, status, Request
from src.utils.env_config import config

# SPHINX
from src.exceptions.exceptions import (
    UnauthorizedError,
    ForbiddenError,
    BadRequestError,
    InternalServerError,
)
from src.i18n.i18n_resolver import i18nResolver as i18n
from src.utils.language_identifier import get_language_from_request
from src.interfaces.controllers.base_controller.interface import IController
from src.utils.json_encoder.date_encoder import DateEncoder


class BaseController(IController):
    @staticmethod
    def run(callback: callable, payload: Optional[dict], request: Request) -> Response:
        lang = get_language_from_request(request=request)
        try:
            response_metadata = callback(payload)
            payload = BaseController.create_response_payload(
                response_metadata=response_metadata, lang=lang
            )
            return Response(
                content=json.dumps(payload, cls=DateEncoder),
                status_code=response_metadata.get("status_code"),
            )
        except UnauthorizedError as e:
            return BaseController.compile_error_response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message=i18n.get_translate(str(e), locale=lang),
            )
        except ForbiddenError as e:
            return BaseController.compile_error_response(
                status_code=status.HTTP_403_FORBIDDEN,
                message=i18n.get_translate(str(e), locale=lang),
            )
        except BadRequestError as e:
            return BaseController.compile_error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=i18n.get_translate(str(e), locale=lang),
            )
        except InternalServerError as e:
            return BaseController.compile_error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=i18n.get_translate(str(e), locale=lang),
            )
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            return BaseController.compile_error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=i18n.get_translate("internal_error", locale=lang),
            )

    @staticmethod
    def compile_error_response(status_code: status, message: str):
        return Response(
            content=json.dumps({"detail": [{"msg": message}]}), status_code=status_code
        )

    @staticmethod
    def create_response_payload(response_metadata: dict, lang: str) -> dict:
        payload = dict()
        if "message_key" in response_metadata:
            payload.update(
                {
                    "message": i18n.get_translate(
                        response_metadata.get("message_key"), locale=lang
                    )
                }
            )
        if "payload" in response_metadata:
            payload.update(response_metadata.get("payload"))
        return payload
