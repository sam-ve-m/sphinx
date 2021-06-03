from decouple import config
from fastapi import status

from src.repositories.file.repository import FileRepository, FileType


class TermsService:
    @staticmethod
    def save_term(
        payload: dict,
        file_repository=FileRepository(bucket_name=config("AWS_BUCKET_TERMS")),
    ):
        file_type = payload.get('file_type')
        file_repository.save_term_file(
            file_type=eval(f'FileType.{file_type.upper()}'),
            content=payload.get("file_or_base64")
        )
        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "files.uploaded",
        }
