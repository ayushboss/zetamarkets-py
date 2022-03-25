from enum import Enum


class EventType(Enum):
    # Refers to events that reflect a change in the exchange state.
    EXCHANGE = "exchange"
    # Expiration event for a zeta group.
    EXPIRY = "expiry"
    """
    Events that reflect a change in user state
    i.e. Margin account or orders
    """
    USER = "user"
    # A change in the clock account.
    CLOCK = "clock"
    # A change in the greek account.
    GREEKS = "greeks"
    # A trade event for the user margin account.
    TRADE = "trade"
    # An update in the orderbook.
    ORDERBOOK = "orderbook"
    # On oracle account change.
    ORACLE = "oracle"
