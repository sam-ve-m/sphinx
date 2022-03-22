from etria_logger import GLADSHEIM_LOGGING_CONFIG

import uvicorn
from fastapi import FastAPI

# SPHINX
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructures.env_config import config
from src.routers.routes_registers import (
    UserRouter,
    ThirdPartRouter,
    AdminRouter,
    ClientRouter,
    PublicRouter,
)

# This import is extremely important for load all routes
from src.routers import *

app = FastAPI(root_path=config("ROOT_PATH"))

UserRouter.apply_middleware(app)
app.include_router(UserRouter.instance())

ThirdPartRouter.apply_middleware(app)
app.include_router(ThirdPartRouter.instance())

AdminRouter.apply_middleware(app)
app.include_router(AdminRouter.instance())

ClientRouter.apply_middleware(app)
app.include_router(ClientRouter.instance())

PublicRouter.apply_middleware(app)
app.include_router(PublicRouter.instance())


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        access_log=True,
        log_config=GLADSHEIM_LOGGING_CONFIG,
        root_path=config("ROOT_PATH"),
    )
