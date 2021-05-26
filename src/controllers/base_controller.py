from typing import Optional
from src.exceptions.exceptions import (
    UnauthorizedError,
    ForbiddenError,
    BadRequestError,
    InternalServerError
)
from fastapi import Response, status, Request
from src.i18n.i18n_resolver import i18nResolver as i18n
from src.utils.language_identifier import get_language_from_request
import json


class BaseController:

    @staticmethod
    def run(callback: callable, payload: Optional[dict], request: Request):
        lang = get_language_from_request(request=request)
        try:
            response_metadata = callback(payload)
            return Response(
                content=json.dumps({"message": i18n.get_translate(response_metadata.get('message_key'), locale=lang)}),
                status_code=response_metadata.get('status_code')
            )
        except UnauthorizedError as e:
            return Response(
                content=json.dumps({"message": i18n.get_translate(str(e), locale=lang)}),
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        except ForbiddenError as e:
            return Response(
                content=json.dumps({"message": i18n.get_translate(str(e), locale=lang)}),
                status_code=status.HTTP_403_FORBIDDEN
            )
        except BadRequestError as e:
            return Response(
                content=json.dumps({"message": i18n.get_translate(str(e), locale=lang)}),
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except InternalServerError as e:
            return Response(
                content=json.dumps({"message": i18n.get_translate(str(e), locale=lang)}),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except:
            return Response(
                content=json.dumps({"message": i18n.get_translate('internal_error', locale=lang)}),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
