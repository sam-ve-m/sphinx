from bs4 import BeautifulSoup as bs
import tempfile
import os
from etria_logger import Gladsheim

from src.domain.email.templates.enum import EmailTemplate


class HtmlModifier:
    def __init__(self, email_template: EmailTemplate, content: dict):
        self.base = "src/services/asset"
        with open(
            os.path.join(self.base, f"{email_template.value}.html")
        ) as html_template:
            self.html = html_template.read()
        self.content = content

    def modify(self):
        try:
            for field, value in self.content.items():
                self.html = self.html.replace("{{" f"{field}" "}}", value)
        except Exception as e:
            Gladsheim.error(error=e)

    def return_email_content(self):
        return self.html

    def __call__(self):
        self.modify()
        return self.return_email_content()
