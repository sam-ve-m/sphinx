from fastapi import APIRouter,  Request
from src.routers.validators.base import Feature
from src.controllers.base_controller import BaseController
from src.utils.jwt_utils import JWTHandler
from src.controllers.purchases.controller import PurchaseController

router = APIRouter()


@router.put("/purchase", tags=["purchase"])
def add_features_to_user(feature: Feature, request: Request):
    payload = {
        "thebes_answer": JWTHandler.get_payload_from_request(request=request),
        "feature": dict(feature).get("feature"),
    }
    return BaseController.run(PurchaseController.add_feature, dict(payload), request)



@router.delete("/purchase", tags=["purchase"])
def remove_features_to_user(feature: Feature, request: Request):
    payload = {
        "thebes_answer": JWTHandler.get_payload_from_request(request=request),
        "feature": dict(feature).get("feature"),
    }
    return BaseController.run(PurchaseController.delete_feature, dict(payload), request)

