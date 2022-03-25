from src.services.bank_account.service import UserBankAccountService


class UserBankAccounts:

    @staticmethod
    async def create(payload: dict):
        create_account_response = await UserBankAccountService.create_user_bank_accounts(payload=payload)
        return create_account_response

    @staticmethod
    async def update(payload: dict):
        update_bank_account_response = await UserBankAccountService.update_user_bank_account(payload=payload)
        return update_bank_account_response

    @staticmethod
    async def get(payload: dict):
        get_user_bank_accounts_response = await UserBankAccountService.get_user_bank_accounts(payload=payload)
        return get_user_bank_accounts_response

    @staticmethod
    async def delete(payload: dict):
        delete_bank_account_response = await UserBankAccountService.delete_user_bank_account(payload=payload)
        return delete_bank_account_response
