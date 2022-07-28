from enum import Enum


class CanBeOperatedByLegalAttorney(Enum):
    PORTFOLIO_MANAGER = 1
    ATTORNEY = 2
    LEGAL_REPRESENTATIVE = 3
    NO = 4
