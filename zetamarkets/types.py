from enum import Enum


class OrderType(Enum):
    LIMIT = "limit"
    POSTONLY = "postonly"
    FILLORKILL = "fillorkill"


class Side(Enum):
    BID = "bid"
    ASK = "ask"


class Kind(Enum):
    UNINITIALIZED = "uninitialized"
    CALL = "call"
    PUT = "put"
    FUTURE = "future"


class MarginType(Enum):
    INITIAL = "initial"
    MAINTENANCE = "maintenance"


class ProgramAccountType(Enum):
    MARGINACCOUNT = "MarginAccount"
