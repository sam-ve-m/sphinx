import json

from fastapi import FastAPI, Request, status, Response
import uvicorn
from src.utils.jwt_utils import JWTHandler

from src.routers.user import router as UserRouter
from src.routers.feature import router as FeatureRouter
from src.routers.authenticate import router as AuthenticateRouter
from src.routers.pendencies import router as PendenciesRouter
from src.routers.purchase import router as PurchaseRouter
from src.routers.view import router as ViewRouter
from src.i18n.i18n_resolver import i18nResolver as i18n
from src.utils.language_identifier import get_language_from_request

app = FastAPI()


@app.middleware("http")
async def process_thebes_answer(request: Request, call_next):
    # TODO: VALIDRA DO BANCO DELETE E TOKEN VALID AFTER
    if is_public(request=request):
        pass
    else:
        try:
            if need_be_admin(request=request):
                raise Exception("Not allowed")
        except:
            response = Response(
                content=json.dumps(
                    {
                        "message": i18n.get_translate(
                            "invalid_token",
                            locale=get_language_from_request(request=request),
                        )
                    }
                ),
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
            return response
    return await call_next(request)


def is_public(request: Request):
    return request.method == "POST" and request.url.path in [
        "/user",
        "/user/forgot_password",
        "/login",
        "/login/admin",
    ]


def need_be_admin(request: Request):
    thebes_answer = JWTHandler.get_payload_from_request(request=request)
    data = JWTHandler.decrypt_payload(thebes_answer)
    return (
        request.url.path == "/user_admin"
        or request.url.path.startswith("/view")
        or request.url.path.startswith("/feature")
    ) and data.get("is_admin") is not True


app.include_router(UserRouter)
app.include_router(FeatureRouter)
app.include_router(AuthenticateRouter)
app.include_router(PendenciesRouter)
app.include_router(AuthenticateRouter)
app.include_router(PurchaseRouter)
app.include_router(ViewRouter)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
