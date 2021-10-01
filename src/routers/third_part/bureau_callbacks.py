# OUTSIDE LIBRARIES
from fastapi import Request

# SPHINX
from src.routers.routes_registers.third_part import ThirdPartRouter
from src.domain.validators.bureaux_callbacks_validators import BureauCallback
from src.controllers.base_controller import BaseController
from src.controllers.bureau_callbacks.bureau_callback import BureauCallbackController

router = ThirdPartRouter.instance()


@router.put("/bureau_callback", tags=["bureau_callback"])
def user_bureau_callback(bureau_callback: BureauCallback, request: Request):
    return BaseController.run(
        BureauCallbackController.process_callback, bureau_callback.dict(), request
    )
