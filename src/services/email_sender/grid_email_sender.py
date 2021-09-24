import sendgrid
from sendgrid.helpers.mail import Email, To, Content, Mail
from src.utils.env_config import config
import logging

from src.exceptions.exceptions import InternalServerError
from src.core.interfaces import IEmailSender


class EmailSender(IEmailSender):
    sg = sendgrid.SendGridAPIClient(api_key=config("MAIL_KEY"))
    sender_email = Email(config("MAIL_SENDER"))

    @staticmethod
    def send_email_to(target_email: str, message: str, subject: str) -> None:
        try:
            message = Content("text/html", message)
            mail = Mail(
                from_email=EmailSender.sender_email,
                to_emails=To(target_email),
                subject=subject,
                html_content=message,
            )
            EmailSender.sg.client.mail.send.post(request_body=mail.get())
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            raise InternalServerError("email.trouble.send")
