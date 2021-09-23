# OUTSIDE LIBRARIES
import uvicorn
from fastapi import FastAPI, Request, Response

# SPHINX
from src.routers.user import router as user_router
from src.routers.feature import router as feature_router
from src.routers.authenticate import router as authenticate_router
from src.routers.term import router as term_router
from src.routers.suitability import router as suitability_router
from src.routers.view import router as view_router
from src.routers.client_register_enums import router as client_register_enums_router
from src.routers.bureau_callbacks import router as bureau_callbacks_router
from src.utils.middleware import (
    route_is_third_part_access,
    route_is_public,
    check_if_is_user_not_allowed_to_access_route,
    check_if_third_party_user_is_not_allowed_to_access_route,
)
from src.utils.jwt_utils import JWTHandler

from src.domain.sphinx_constants import *
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]


@app.middleware("http")
async def process_thebes_answer(request: Request, call_next):
    is_third_part_access = route_is_third_part_access(
        url_request=request.url.path,
        third_part_access_path=THIRD_PART_ACCESS_PATH,
        method=request.method,
    )
    if is_third_part_access:
        return await resolve_third_part_request(request=request, call_next=call_next)
    is_public = route_is_public(url_request=request.url.path, method=request.method)
    if not is_public:
        return await resolve_not_public_request(request=request, call_next=call_next)
    return await call_next(request)


async def resolve_third_part_request(request: Request, call_next):
    response = check_if_third_party_user_is_not_allowed_to_access_route(request=request)
    if type(response) == Response:
        return response
    return await call_next(request)


async def resolve_not_public_request(request: Request, call_next):
    jwt_data_or_error_response = JWTHandler.get_thebes_answer_from_request(request=request)
    if type(jwt_data_or_error_response) == Response:
        return jwt_data_or_error_response
    response = check_if_is_user_not_allowed_to_access_route(
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
app.include_router(suitability_router)
app.include_router(term_router)
app.include_router(client_register_enums_router)
app.include_router(bureau_callbacks_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        access_log=True,
        log_config="./log.ini",
        log_level="info",
    )
