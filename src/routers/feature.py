from fastapi import APIRouter

router = APIRouter()


@router.post("/feature", tags=["feature"])
async def create_feature():
    return 200


@router.put("/feature/{feature_id}", tags=["feature"])
async def update_feature_data(feature_id: str):
    return feature_id, 200


@router.delete("/feature/{feature_id}", tags=["feature"])
async def delete_feature(feature_id: str):
    return feature_id, 200
