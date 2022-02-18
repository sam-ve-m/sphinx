# STANDARD LIBS
from abc import ABC, abstractmethod
from typing import Optional, Union
from enum import Enum


# SPHINX
from src.repositories.cache.redis import RepositoryRedis
from src.repositories.file.enum.term_file import TermsFileType
from src.repositories.file.enum.user_file import UserFileType


class IFile(ABC):
    @staticmethod
    @abstractmethod
    def validate_bucket_name(bucket_name: str) -> str:
        pass

    @abstractmethod
    def save_user_file(
        self,
        file_type: UserFileType,
        content: Union[str, bytes],
        user_email: str,
    ) -> str:
        pass

    @abstractmethod
    def save_term_file(
        self, file_type: TermsFileType, content: Union[str, bytes]
    ) -> None:
        pass

    @abstractmethod
    def get_term_file(
        self, file_type: TermsFileType, cache=RepositoryRedis, ttl: int = 0
    ) -> Union[str, dict]:
        pass

    @staticmethod
    @abstractmethod
    def resolve_content(content: Union[str, bytes]) -> Union[str, bytes]:
        pass

    @staticmethod
    @abstractmethod
    def resolve_user_path(user_email: str, file_type: UserFileType) -> str:
        pass

    @staticmethod
    @abstractmethod
    def resolve_term_path(file_type: TermsFileType) -> str:
        pass

    @staticmethod
    @abstractmethod
    async def get_file_extension_by_type(file_type: Enum) -> Optional[str]:
        pass

    @abstractmethod
    def get_current_term_version(self, file_type: TermsFileType) -> int:
        pass

    @abstractmethod
    def _get_last_saved_file_from_folder(self, path: str) -> Optional[str]:
        pass

    @abstractmethod
    def get_user_selfie(
        self, file_type: UserFileType, user_email: str
    ) -> Union[str, dict]:
        pass
