import json

from fastapi import FastAPI, Request, status, Response
import uvicorn
from src.utils.jwt_utils import JWTHandler

from src.routers.user import router as UserRouter
from src.routers.feature import router as FeatureRouter
from src.routers.authenticate import router as AuthenticateRouter
from src.routers.authorization import router as AuthorizationRouter
from src.routers.pendencies import router as PendenciesRouter
from src.routers.purchase import router as PurchaseRouter
from src.routers.view import router as ViewRouter
from src.i18n.i18n_resolver import i18nResolver as i18n

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    if (
            request.method == 'POST' and
            request.url.path in ['/user', '/user/forgot_password', '/login', '/login/admin']
    ):
            response = await call_next(request)
    else:
        token = None
        for header_tuple in request.headers.raw:
            if b'token' in header_tuple:
                token = header_tuple[1].decode()
                break
        try:
            payload = JWTHandler.decrpty_to_paylod(token)
        except Exception:
            response = Response(
                content=json.dumps({"message": i18n.get_translate('invalid_token', locale='pt')}),
                status_code=status.HTTP_401_UNAUTHORIZED
            )
            return response
        response = await call_next(request)
    return response

app.include_router(UserRouter)
app.include_router(FeatureRouter)
app.include_router(AuthenticateRouter)
app.include_router(AuthorizationRouter)
app.include_router(PendenciesRouter)
app.include_router(AuthenticateRouter)
app.include_router(PurchaseRouter)
app.include_router(ViewRouter)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
