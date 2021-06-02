from abc import ABC, abstractmethod


class IEmailSender(ABC):
    @staticmethod
    @abstractmethod
    def send_email_to(target_email: str, message: str, subject: str) -> None:
        pass
