from src.utils.jwt_utils import JWTHandler


class StubMist:
    def validate_jwt(self, jwt):
        pass

    def decrypt_payload(self, jwt):
        pass


class StubHeimdall:
    def decrypt_payload(self, jwt):
        pass


class StubJWT:
    def encode(self, *args):
        pass


class StubJWTHandler(JWTHandler):
    instance = StubJWT()
    mist = StubMist()
    heimdall = StubHeimdall()
