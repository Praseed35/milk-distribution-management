from enum import Enum


class UserRole(str, Enum):

    OWNER = "OWNER"

    CHECKER = "CHECKER"

    DELIVERY_PARTNER = "DELIVERY_PARTNER"