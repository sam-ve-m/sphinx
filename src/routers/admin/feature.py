from fastapi import Request
from src.routers.validators.feature_validators import Feature
from src.controllers.base_controller import BaseController
from src.controllers.features.controller import FeatureController
from src.routers.routes_registers.admin import AdminRouter

router = AdminRouter.instance()


@router.post("/feature", tags=["feature"])
def create_feature(feature: Feature, request: Request):
    return BaseController.run(FeatureController.create, dict(feature), request)


@router.put("/feature/{feature_id}", tags=["feature"])
def update_feature_data(feature_id: str, feature: Feature, request: Request):
    return BaseController.run(
        FeatureController.update,
        {"feature_id": feature_id, "model": dict(feature)},
        request,
    )


@router.delete("/feature/{feature_id}", tags=["feature"])
def delete_feature(feature_id: str, request: Request):
    return BaseController.run(
        FeatureController.update, {"feature_id": feature_id}, request
    )
