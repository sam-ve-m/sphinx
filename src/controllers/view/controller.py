from src.services.views.service import ViewService


class ViewController:

    @staticmethod
    def create(payload: dict):
        return ViewService.create(payload=payload)

    @staticmethod
    def update(payload: dict):
        return ViewService.update(payload=payload)

    @staticmethod
    def delete(payload: dict):
        return ViewService.delete(payload=payload)

    @staticmethod
    def link_feature(payload: dict):
        return ViewService.link_feature(payload=payload)

    @staticmethod
    def get_view(payload: dict):
        return ViewService.get_view(payload=payload)
