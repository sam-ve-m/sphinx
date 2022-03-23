# STANDARD LIBS
from typing import Optional
from etria_logger import Gladsheim
import json

# OUTSIDE LIBRARIES
from fastapi import Response, status, Request
from src.infrastructures.env_config import config

# SPHINX
from src.exceptions.exceptions import (
    UnauthorizedError,
    ForbiddenError,
    BadRequestError,
    InternalServerError,
)
from src.i18n.i18n_resolver import i18nResolver as i18n
from src.core.interfaces.controllers.base_controller.interface import IController
from nidavellir import Sindri


class BaseController(IController):
    @staticmethod
    async def run(
        callback: callable, payload: Optional[dict], request: Request
    ) -> Response:
        lang = i18n.get_language_from_request(request=request)
        try:
            response_metadata = await callback(payload)
            payload = await BaseController.create_response_payload(
                response_metadata=response_metadata, lang=lang
            )
            return Response(
                content=json.dumps(payload, default=Sindri.resolver),
                status_code=response_metadata.get("status_code"),
                headers={"Content-type": "application/json"},
            )
        except UnauthorizedError as e:
            return await BaseController.compile_error_response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message=i18n.get_translate(str(e), locale=lang),
            )
        except ForbiddenError as e:
            return await BaseController.compile_error_response(
                status_code=status.HTTP_403_FORBIDDEN,
                message=i18n.get_translate(str(e), locale=lang),
            )
        except BadRequestError as e:
            return await BaseController.compile_error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=i18n.get_translate(str(e), locale=lang),
            )
        except InternalServerError as e:
            return await BaseController.compile_error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=i18n.get_translate(str(e), locale=lang),
            )
        except Exception as e:
            Gladsheim.error(error=e)
            return await BaseController.compile_error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=i18n.get_translate("internal_error", locale=lang),
            )

    @staticmethod
    async def compile_error_response(status_code: status, message: str):
        return Response(
            content=json.dumps({"detail": [{"msg": message}]}),
            status_code=status_code,
            headers={"Content-type": "application/json"},
        )

    @staticmethod
    async def create_response_payload(response_metadata: dict, lang: str) -> dict:
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
