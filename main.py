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
    if request.method == "POST" and request.url.path in [
        "/user",
        "/user/forgot_password",
        "/login",
        "/login/admin",
    ]:
        response = await call_next(request)
    else:
        thebes_answer = None
        for header_tuple in request.headers.raw:
            if b"thebes_answer" in header_tuple:
                thebes_answer = header_tuple[1].decode()
                break
        try:
            JWTHandler.decrpty_to_paylod(thebes_answer)
        except:
            lang = get_language_from_request(request=request)
            response = Response(
                content=json.dumps(
                    {"message": i18n.get_translate("invalid_token", locale=lang)}
                ),
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
            return response
        response = await call_next(request)
    return response


app.include_router(UserRouter)
app.include_router(FeatureRouter)
app.include_router(AuthenticateRouter)
app.include_router(PendenciesRouter)
app.include_router(AuthenticateRouter)
app.include_router(PurchaseRouter)
app.include_router(ViewRouter)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
