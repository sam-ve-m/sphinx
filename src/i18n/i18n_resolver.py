import i18n
import os
from fastapi import Request

base_path = os.path.dirname(__file__)
i18n.load_path.append(f"{base_path}{os.sep}translate")


class i18nResolver:

    file_name = "translate"

    @staticmethod
    def get_translate(key: str, locale: str):
        return i18n.t(f"{i18nResolver.file_name}.{key}", locale=locale)

    @staticmethod
    def get_language_from_request(request: Request):
        language = None
        for header_tuple in request.headers.raw:
            if b"language" in header_tuple:
                language = header_tuple[1].decode()
                break
        if language and language.lower() in ["pt", "pt_br", "br"]:
            return "pt"
        return "en"
