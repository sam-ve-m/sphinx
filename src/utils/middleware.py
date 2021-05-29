from fastapi import Request, Response


from src.repositories.user.repository import UserRepository
from src.utils.jwt_utils import JWTHandler


def is_public(request: Request):
    return request.method == "POST" and request.url.path in [
        "/user",
        "/user/forgot_password",
        "/login",
        "/login/admin",
    ]


def need_be_admin(request: Request):
    return (
        request.url.path == "/user_admin"
        or request.url.path.startswith("/view")
        or request.url.path.startswith("/feature")
    )


def need_be_admin(request: Request):
    return (
        request.url.path == "/user_admin"
        or request.url.path.startswith("/view")
        or request.url.path.startswith("/feature")
    )


def is_deleted(user_data: dict) -> bool:
    try:
        return user_data.get("deleted")
    except:
        return False


def token_expired(user_data: dict, jwt_data: dict) -> bool:
    token_valid_after = user_data.get("token_valid_after")
    token_created_at = jwt_data.get("created_at")
    return token_valid_after < token_created_at


def validate_user_and_token(request: Request, user_repository = UserRepository()):

    jwt_data = JWTHandler.get_payload_from_request(request=request)
    print(jwt_data)
    print(jwt_data["email"])
    user_data = user_repository.find_one({"email", jwt_data["email"]})
    if is_deleted(user_data=user_data):
        return "invalid_token"
    if token_expired(user_data=user_data, jwt_data=jwt_data):
        return "invalid_token"
