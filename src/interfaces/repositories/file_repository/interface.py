from abc import ABC, abstractmethod
from typing import Optional, Union

from src.repositories.cache.redis import RepositoryRedis
from src.repositories.file.repository import TermsFileType, UserFileType


class IFile(ABC):

    @abstractmethod
    def validate_bucket_name(bucket_name: str) -> str:
       pass

    @abstractmethod
    def save_user_file(
        self, file_type: UserFileType, content: Union[str, bytes], user_email: str,
    ) -> None:
        pass

    @abstractmethod
    def save_term_file(
        self, file_type: TermsFileType, content: Union[str, bytes]
    ) -> None:
       pass

    @abstractmethod
    def get_term_file(
        self, file_type: TermsFileType, cache=RepositoryRedis
    ) -> Optional[str]:
        pass

    @abstractmethod
    def resolve_content(content: Union[str, bytes]):
        pass

    @abstractmethod
    def resolve_user_path(user_email: str, file_type: UserFileType) -> str:
        pass

    @abstractmethod
    def resolve_term_path(file_type: TermsFileType) -> str:
        pass

    @abstractmethod
    def get_file_extension_by_type(file_type: TermsFileType) -> Optional[str]:
        pass

    @abstractmethod
    def get_term_version(self, file_type: TermsFileType, is_new_version=False) -> int:
        pass

    @abstractmethod
    def _get_last_saved_file_from_folder(self, path: str) -> Optional[str]:
      pass
