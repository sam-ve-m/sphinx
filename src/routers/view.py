from fastapi import APIRouter

router = APIRouter()


@router.post("/view", tags=["view"])
async def create_view():
    return 200


@router.put("/view/{view_id}", tags=["view"])
async def update_view(view_id: str):
    return view_id, 200


@router.delete("/view/{view_id}", tags=["view"])
async def delete_view(view_id: str):
    return view_id, 200


@router.put("/view/{view_id}/{feature_id}", tags=["view"])
async def link_feature(view_id: str, feature_id: str):
    return view_id, feature_id, 200


@router.get("/view/{view_id}", tags=["view"])
async def get_view(view_id: str):
    return view_id, 200

