from src.services.purchases.service import PurchaseService


class PurchaseController:
    @staticmethod
    def add_feature(payload: dict):
        return PurchaseService.add_feature(payload=payload)

    @staticmethod
    def delete_feature(payload: dict):
        return PurchaseService.delete_feature(payload=payload)
