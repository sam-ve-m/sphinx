from src.services.terms.service import TermsService


class TermsController:
    @staticmethod
    async def save_term(payload: dict):
        return await TermsService.save_term(payload=payload)

    @staticmethod
    async def get_term(payload: dict):
        return await TermsService.get_term(payload=payload)

    @staticmethod
    async def get_terms(payload: dict):
        return await TermsService.get_terms(payload=payload)
