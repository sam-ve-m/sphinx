from i18n.translator import Translator
import os


base_path = os.path.dirname(os.path.abspath(__file__))
supported_languages = ['en_US', 'pt_BR']
tr = Translator(f'{base_path}{os.sep}translations', supported_languages, 'en_US')


# class i18nResolver:
#
#     @staticmethod
#     def get_translate(key: str, locale: str):
#         return i18n.t(f'{locale}.{key}')
#


# a = i18nResolver.get_translate('invalid_token', locale='en')
b = tr._('Hello world!')
input()
