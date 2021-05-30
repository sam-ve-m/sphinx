import uvicorn
from fastapi import FastAPI, Request, status, Response
from starlette.types import ASGIApp, Scope, Receive, Send
import json


from src.routers.user import router as user_router
from src.routers.feature import router as feature_router
from src.routers.authenticate import router as authenticate_router
from src.routers.pendencies import router as pendencies_router
from src.routers.purchase import router as purchase_router
from src.routers.view import router as view_router
from src.i18n.i18n_resolver import i18nResolver as i18n
from src.utils.language_identifier import get_language_from_request
from src.utils.middleware import is_public, validate_user_and_admin_routes


app = FastAPI()


@app.middleware("http")
async def process_thebes_answer(request: Request, call_next):
    is_not_public = is_public(request=request) is False
    if is_not_public:
        user_not_allowed = validate_user_and_admin_routes(request=request)
        if user_not_allowed:
            return Response(
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
    return await call_next(request)


app.include_router(user_router)
app.include_router(feature_router)
app.include_router(authenticate_router)
app.include_router(pendencies_router)
app.include_router(authenticate_router)
app.include_router(purchase_router)
app.include_router(view_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, access_log=True, log_config="./log.ini", log_level="info")
