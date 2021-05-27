import i18n
import os

base_path = os.path.dirname(__file__)
i18n.load_path.append(f"{base_path}{os.sep}translate")


class i18nResolver:

    file_name = "translate"

    @staticmethod
    def get_translate(key: str, locale: str):
        return i18n.t(f"{i18nResolver.file_name}.{key}", locale=locale)
