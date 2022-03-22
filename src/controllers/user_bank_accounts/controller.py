from src.services.bank_account.service import UserBankAccountService


class UserBankAccounts:

    @staticmethod
    async def create(payload: dict):
        return await UserBankAccountService.create_user_bank_accounts(payload=payload)

    @staticmethod
    async def update(payload: dict):
        return await UserBankAccountService.update_bank_account(payload=payload)

    @staticmethod
    async def delete(payload: dict):
        return await UserBankAccountService.delete_bank_account(payload=payload)

    @staticmethod
    async def get(payload: dict):
        return await UserBankAccountService.get_user_bank_accounts(payload=payload)



