from src.services.bank_account.service import UserBankAccountService


class UserBankAccounts:

    @staticmethod
    def create(payload: dict):
        return FeatureService.create(payload=payload)

    @staticmethod
    def update(payload: dict):
        return FeatureService.update(payload=payload)

    @staticmethod
    def delete(payload: dict):
        return UserBankAccountService.delete(payload=payload)

    @staticmethod
    def get(payload: dict):
        return await UserBankAccountService.get_user_bank_accounts(payload=payload)
