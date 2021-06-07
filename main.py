# OUTSIDE LIBRARIES
import uvicorn
from fastapi import FastAPI, Request, status, Response

# SPHINX
from src.routers.user import router as user_router
from src.routers.feature import router as feature_router
from src.routers.authenticate import router as authenticate_router
from src.routers.pendencies import router as pendencies_router
from src.routers.term import router as term_router
from src.routers.suitability import router as suitability_router
from src.routers.view import router as view_router
from src.utils.middleware import is_public, is_user_not_allowed
from src.utils.jwt_utils import JWTHandler

app = FastAPI()


@app.middleware("http")
async def process_thebes_answer(request: Request, call_next):
    is_not_public = is_public(request=request) is False
    if is_not_public:
        jwt_data_or_error_response = JWTHandler.get_payload_from_request(
            request=request
        )
        if type(jwt_data_or_error_response) == Response:
            return jwt_data_or_error_response
        response = is_user_not_allowed(
            request=request, jwt_data=jwt_data_or_error_response
        )
        if type(response) == Response:
            return response
    return await call_next(request)


app.include_router(user_router)
app.include_router(feature_router)
app.include_router(authenticate_router)
app.include_router(view_router)
app.include_router(authenticate_router)
app.include_router(pendencies_router)
app.include_router(suitability_router)
app.include_router(term_router)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        access_log=True,
        log_config="./log.ini",
        log_level="info",
    )
