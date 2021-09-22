# STANDARD LIBS
from typing import Union, List, Optional

# OUTSIDE LIBRARIES
from fastapi import APIRouter, Request, Response
from pydantic import BaseModel

# SPHINX

from src.controllers.base_controller import BaseController
from src.controllers.bureau_callbacks.bureau_callback import BureauCallbackController
from src.routers.validators.bureaux_callbacks_validators import BureauCallback

router = APIRouter()


@router.put("/bureau_callback", tags=["bureau_callback"])
def user_bureau_callback(bureau_callback: BureauCallback, request: Request):
    return BaseController.run(
        BureauCallbackController.process_callback, bureau_callback.dict(), request
    )
