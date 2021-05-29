import uvicorn
from fastapi import FastAPI, Request, status, Response

from fastapi_cache import caches, close_caches
from fastapi_cache.backends.memory import CACHE_KEY, InMemoryCacheBackend
import json


from src.routers.user import router as user_router
from src.routers.feature import router as feature_router
from src.routers.authenticate import router as authenticate_router
from src.routers.pendencies import router as pendencies_router
from src.routers.purchase import router as purchase_router
from src.routers.view import router as view_router
from src.i18n.i18n_resolver import i18nResolver as i18n
from src.utils.jwt_utils import JWTHandler
from src.utils.language_identifier import get_language_from_request
from src.utils.middleware import is_public, need_be_admin


app = FastAPI()


@app.on_event('startup')
async def on_startup() -> None:
    rc = InMemoryCacheBackend()
    caches.set(CACHE_KEY, rc)


@app.on_event('shutdown')
async def on_shutdown() -> None:
    await close_caches()


@app.middleware("http")
async def process_thebes_answer(request: Request, call_next):
    # # TODO: VALIDRA DO BANCO DELETE E TOKEN VALID AFTER
    # if is_public(request=request) is False:
    #     thebes_answer = JWTHandler.get_payload_from_request(request=request)
    #     data = JWTHandler.decrypt_payload(thebes_answer)
    #     if need_be_admin(request=request) and data.get("is_admin") is False:
    #         response = Response(
    #             content=json.dumps(
    #                 {
    #                     "message": i18n.get_translate(
    #                         "invalid_token",
    #                         locale=get_language_from_request(request=request),
    #                     )
    #                 }
    #             ),
    #             status_code=status.HTTP_401_UNAUTHORIZED,
    #         )
    #         return response
    return await call_next(request)


app.include_router(user_router)
app.include_router(feature_router)
app.include_router(authenticate_router)
app.include_router(pendencies_router)
app.include_router(authenticate_router)
app.include_router(purchase_router)
app.include_router(view_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
