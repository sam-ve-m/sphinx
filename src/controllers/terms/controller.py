from src.services.terms.service import TermsService


class TermsController:
    @staticmethod
    def save_term(payload: dict):
        return TermsService.save_term(payload=payload)
