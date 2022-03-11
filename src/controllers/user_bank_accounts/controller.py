from src.services.bank_account.service import UserBankAccountService


class UserBankAccounts:

    @staticmethod
    def create(payload: dict):
        return UserBankAccountService.create_user_bank_accounts(payload=payload)

    @staticmethod
    def update(payload: dict):
        return UserBankAccountService.update_user_bank_accounts(payload=payload)

    @staticmethod
    def delete(payload: dict):
        return UserBankAccountService.delete_user_bank_accounts(payload=payload)

    @staticmethod
    def get(payload: dict):
        return await UserBankAccountService.get_user_bank_accounts(payload=payload)
