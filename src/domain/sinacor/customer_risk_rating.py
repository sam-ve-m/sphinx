from enum import Enum


class CustomerRiskRating(Enum):
    PORTFOLIO_MANAGER = 1
    ATTORNEY = 2
    LEGAL_REPRESENTATIVE = 3
    NO = 4
