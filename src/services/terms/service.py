# OUTSIDE LIBRARIES
from src.utils.env_config import config
from fastapi import status

# SPHINX
from src.repositories.file.repository import FileRepository
from src.interfaces.services.term.interface import ITerm
from src.repositories.file.enum.term_file import TermsFileType


class TermsService(ITerm):
    @staticmethod
    def save_term(
        payload: dict,
        file_repository=FileRepository(bucket_name=config("AWS_BUCKET_TERMS")),
    ):
        file_type = payload.get("file_type")
        file_repository.save_term_file(
            file_type=file_type, content=payload.get("file_or_base64"),
        )
        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "files.uploaded",
        }

    @staticmethod
    def get_term(
        payload: dict,
        file_repository=FileRepository(bucket_name=config("AWS_BUCKET_TERMS")),
    ):
        link = file_repository.get_term_file(file_type=payload.get("file_type"))
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"link": link},
        }

    @staticmethod
    def get_terms(payload: dict):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {
                "terms": [term_enum.value for term_enum in list(TermsFileType)]
            },
        }
