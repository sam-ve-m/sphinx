import sendgrid
from sendgrid.helpers.mail import Email, To, Content, Mail
from decouple import config


class EmailSender:
    sg = sendgrid.SendGridAPIClient(api_key=config("MAIL_KEY"))
    sender_email = Email(config('MAIL_SENDER'))

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
        except Exception as err:
            print(err)


if __name__ == '__main__':
    EmailSender.send_email_to(target_email='msa@lionx.com.br', message='oi', subject='Test')
