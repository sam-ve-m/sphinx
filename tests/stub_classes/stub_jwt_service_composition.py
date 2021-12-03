from src.services.jwts.service import JwtService


class StubMist:
    def validate_jwt(self, jwt):
        pass

    def decrypt_payload(self, jwt):
        pass


class StubHeimdall:
    def decode_payload(self, jwt):
        pass


class StubJWT:
    def encode(self, *args):
        pass


class JwtServiceWithStubAttributes(JwtService):
    instance = StubJWT()
    mist = StubMist()
    heimdall = StubHeimdall()
