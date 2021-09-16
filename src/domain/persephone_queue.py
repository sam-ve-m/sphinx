from enum import Enum


class PersephoneQueue(Enum):
    PROSPECT_USER_QUEUE = 0
    TERM_QUEUE = 1
    SUITABILITY_QUEUE = 2
    DTVM_USER_QUEUE = 3
    DTVM_UPDATE_USER_QUEUE = 4
    KYC_TABLE_QUEUE = 5
    USER_IDENTIFIER_DATA = 6
    USER_SELFIE = 7
    USER_COMPLEMENTARY_DATA = 8
    USER_GET_QUIZ_FROM_STONEAGE = 9
    USER_SEND_QUIZ_FROM_STONEAGE = 10
    USER_SET_ELECTRONIC_SIGNATURE = 11
    USER_CHANGE_OR_RESET_ELECTRONIC_SIGNATURE = 12
    USER_THEBES_HALL = 13
    USER_ELECTRONIC_SIGNATURE_SESSION = 14
