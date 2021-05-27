from fastapi import Request


def get_language_from_request(request: Request):
    language = None
    for header_tuple in request.headers.raw:
        if b'language' in header_tuple:
            language = header_tuple[1].decode()
            break
    if language and language.lower() in ['pt', 'pt_br', 'br']:
        return 'pt'
    return 'en'
