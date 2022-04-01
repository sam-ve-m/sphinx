from src.services.views.service import ViewService


class ViewController:
    @staticmethod
    async def create(payload: dict):
        return await ViewService.create(payload=payload)

    @staticmethod
    async def update(payload: dict):
        return await ViewService.update(payload=payload)

    @staticmethod
    async def delete(payload: dict):
        return await ViewService.delete(payload=payload)

    @staticmethod
    async def link_feature(payload: dict):
        return await ViewService.link_feature(payload=payload)

    @staticmethod
    async def get(payload: dict):
        return await ViewService.get()

    @staticmethod
    async def delete_link_feature(payload: dict):
        return await ViewService.delete_link_feature(payload=payload)

    @staticmethod
    async def get_view(payload: dict):
        return await ViewService.get_view(payload=payload)
