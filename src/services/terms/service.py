# OUTSIDE LIBRARIES
from src.infrastructures.env_config import config
from fastapi import status

# SPHINX
from src.repositories.file.repository import FileRepository
from src.core.interfaces.services.term.interface import ITerm
from src.repositories.file.enum.term_file import TermsFileType


class TermsService(ITerm):
    @staticmethod
    async def save_term(
        payload: dict,
        file_repository=FileRepository,
    ) -> dict:
        file_type = payload.get("file_type")
        await file_repository.save_term_file(
            file_type=file_type,
            content=payload.get("file_or_base64"),
            bucket_name=config("AWS_BUCKET_TERMS"),
        )
        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "files.uploaded",
        }

    @staticmethod
    async def get_term(
        payload: dict,
        file_repository=FileRepository,
    ) -> dict:
        link = await file_repository.get_term_file(
            file_type=payload.get("file_type"), bucket_name=config("AWS_BUCKET_TERMS")
        )
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"link": link},
        }

    @staticmethod
    async def get_terms(payload: dict) -> dict:
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {
                "terms": [term_enum.value for term_enum in list(TermsFileType)]
            },
        }
