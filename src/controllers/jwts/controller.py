from src.services.jwts.service import JwtService


class JwtController:
    @staticmethod
    def insert_one(jwt: str, email: str):
        return JwtService.insert_one(jwt=jwt, email=email)
