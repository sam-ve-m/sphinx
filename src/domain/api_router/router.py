# Standards
from typing import Callable, List


# Third Part
from fastapi import APIRouter


class SphinxAPIRouter(APIRouter):

    def __init__(self):
        self.__permission_by_route = dict()
        super().__init__()

    def requested_permissions(self, views: List[str], features: List[str]) -> Callable:
        def deco(func: Callable) -> Callable:
            self.__permission_by_route.update({self.routes[-1].path: {
                "views": views,
                "features": features
            }})
            return func
        return deco

    def get_permission_by_route(self, route: str):
        return self.__permission_by_route.get(route)
