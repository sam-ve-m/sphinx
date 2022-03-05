# STANDARD LIBS
from abc import ABC, abstractmethod
from typing import Union

# SPHINX
from src.repositories.file.enum.term_file import TermsFileType
from src.repositories.file.enum.user_file import UserFileType


class IFile(ABC):
    @classmethod
    @abstractmethod
    async def save_user_file(
        cls,
        file_type: UserFileType,
        content: Union[str, bytes],
        unique_id: str,
        bucket_name: str,
    ) -> str:
        pass

    @classmethod
    @abstractmethod
    async def save_term_file(
        cls, file_type: TermsFileType, content: Union[str, bytes], bucket_name: str
    ) -> None:
        pass

    @classmethod
    @abstractmethod
    async def get_term_file(
        cls, file_type: TermsFileType, bucket_name: str, ttl: int = 3600
    ) -> Union[str, dict]:
        pass

    @classmethod
    @abstractmethod
    def get_current_term_version(
        cls, file_type: TermsFileType, bucket_name: str
    ) -> int:
        pass

    @classmethod
    @abstractmethod
    async def get_user_selfie(
        cls,
        file_type: UserFileType,
        unique_id: str,
        bucket_name: str,
    ) -> Union[str, dict]:
        pass
