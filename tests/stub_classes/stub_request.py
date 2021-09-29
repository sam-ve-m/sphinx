from typing import Type, List


class StubURL:
    path = "/"


class StubHeaders:
    def __init__(self):
        self.raw = list()

    def set_headers(self, raw: List[tuple]):
        self.raw = raw


class StubRequest:
    method = "POST"
    headers = StubHeaders()

    def __init__(self, url: Type[StubURL]):
        self.url = url
        self.headers = StubHeaders()