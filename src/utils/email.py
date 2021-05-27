from bs4 import BeautifulSoup as bs
import tempfile
import os


class HtmlModifier:
    def __init__(self, html_path: str, message_text, target_link: str):
        self.base = html_path
        self.html = open(os.path.join(self.base, "email_base.html"))
        self.soup = bs(self.html, "html.parser")
        self.link_a = None
        self.message_text = message_text
        self.target_link = target_link
        self.temp_file = None

    def modify(self):
        new_link = bs(
            f"<a href={self.target_link} id='link-auth'>Clique Aqui!</a>",
            "html.parser",
        )
        new_message_text = bs(
            f"<p id='message_text'>{self.message_text} <a href='' id='link-auth'></a></p>",
            "html.parser",
        )
        self.soup.find("p", {"id": "message_text"}).replace_with(new_message_text)
        self.soup.find("a", {"id": "link-auth"}).replace_with(new_link)
        self.temp_file = tempfile.TemporaryFile(mode="wb+")
        self.temp_file.write(self.soup.prettify("utf-8"))

    def return_email_content(self):
        self.temp_file.seek(0, 0)
        template = self.temp_file.read().decode()
        self.temp_file.close()
        return template

    def __call__(self):
        self.modify()
        return self.return_email_content()
