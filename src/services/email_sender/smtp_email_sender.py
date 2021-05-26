import smtplib, ssl
from decouple import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailSender:

    context = ssl.create_default_context()
    email_provider = smtplib.SMTP(config("DEFAULT_PROVIDER", config("PORT")))
    message = MIMEMultipart("alternative")

    def __init__(self, sender_email: str, sender_passwd: str, html: str) -> None:

        self.sender_email = sender_email
        self.sender_passwd = sender_passwd
        self.message.attach(MIMEText(html, "html"))

    def send_email_to(self, target: str) -> None:
        try:

            self.message["Subject"] = "Teste HTML"
            self.message["From"] = self.sender_email
            self.message["To"] = target
            self.email_provider.ehlo()
            self.email_provider.starttls(context=self.context)
            self.email_provider.ehlo()
            self.email_provider.login(self.sender_email, self.sender_passwd)
            self.email_provider.sendmail(
                self.sender_email, target, self.message.as_string()
            )
        except Exception as err:
            print(err)
        finally:
            self.email_provider.quit()
