from fastapi import Request


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

