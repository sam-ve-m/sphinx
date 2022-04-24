from enum import Enum


class DriveWealthFileType(Enum):
    DRIVER_LICENSE = "DRIVER_LICENSE"
    NATIONAL_ID_CARD = "NATIONAL_ID_CARD"


class DriveWealthFileSide(Enum):
    FRONT = "FRONT"
    BACK = "BACK"
