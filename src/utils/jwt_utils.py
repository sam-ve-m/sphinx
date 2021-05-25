import json
from jwt import JWT, jwk_from_dict, jwk_from_pem


class JWTHandler:

    instance = JWT()

    @staticmethod
    def generate_token(payload: dict):
        with open(r'C:\Users\MS\Documents\LionX\sphinx.lionx.com.br\keys\id_rsa', 'rb') as fh:
            signing_key = jwk_from_pem(fh.read())
        compact_jws = JWTHandler.instance.encode(payload, signing_key, alg='RS256')
        return compact_jws

    @staticmethod
    def decrpty_to_paylod(crypted_payload: str):
        with open(r'C:\Users\MS\Documents\LionX\sphinx.lionx.com.br\keys\id_rsa.json', 'r') as fh:
            verifying_key = jwk_from_dict(json.load(fh))
        payload = JWTHandler.instance.decode(crypted_payload, verifying_key, do_time_check=True)
        return payload
