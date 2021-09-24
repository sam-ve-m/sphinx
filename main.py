# OUTSIDE LIBRARIES
import uvicorn
from fastapi import FastAPI

# SPHINX
from fastapi.middleware.cors import CORSMiddleware

from src.routers.router_registers import (
    UserRouter,
    ThirdPartRouter,
    AdminRouter,
    ClientRouter,
    PublicRouter
)

app = FastAPI()
origins = ["*"]


app.include_router(UserRouter.instance())
app.include_router(ThirdPartRouter.instance())
app.include_router(AdminRouter.instance())
app.include_router(ClientRouter.instance())
app.include_router(PublicRouter.instance())


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
