# OUTSIDE LIBRARIES

# SPHINX
from src.routers.routes_registers.third_part import ThirdPartRouter

router = ThirdPartRouter.instance()

#
# @router.put("/bureau_callback", tags=["bureau_callback"])
# def user_bureau_callback(bureau_callback: BureauCallback, request: Request):
#     return BaseController.run(
#         BureauCallbackController.process_callback, bureau_callback.dict(), request
#     )
