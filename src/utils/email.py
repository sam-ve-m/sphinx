from bs4 import BeautifulSoup as bs
import os

class HtmlModifier:
    def __init__(self, html_path: str, message_text, target_link: str):
        self.base = html_path
        self.html = open(os.path.join(self.base, "email_base.html"))
        self.soup = bs(self.html, "html.parser")
        self.link_a = None
        self.message_text = message_text
        self.target_link = target_link

    def modify(self):
        new_link = bs(
            f"<a href={self.target_link} id='link-auth'>Clique Aqui!</a>",
            "html.parser",
        )
        new_message_text = bs(f"<p id='message_text'>{self.message_text} <a href='' id='link-auth'></a></p>","html.parser")
        self.soup.find("p", {"id": "message_text"}).replace_with(new_message_text)
        self.soup.find("a", {"id": "link-auth"}).replace_with(new_link)

        with open(os.path.join(self.base, "email.html"), "wb") as f_output:
            f_output.write(self.soup.prettify("utf-8"))

    def return_email_content(self):
        with open(os.path.join(self.base, "email.html"), "r") as f:
            template = f.read()
            return template

    def __call__(self):
        self.modify()
        return self.return_email_content()