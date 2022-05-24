import math
class ZetaGroupMarkets:

    def __init__(self):
        # TODO: Update this
        self._expiry_series = None
        self._markets = None
        self._subscribed_market_indexes = None
        self._last_poll_timestamp = 0
        self._subscribed_market_indexes = set()

    @property
    def front_expiry_index(self):
        return self._front_expiry_index

    @property
    def expiry_series(self):
        return self._expiry_series

    @property
    def markets(self):
        return self._markets

    def get_markets_by_expiry_index(self, expiry_index: int):
        head = expiry_index * self.products_per_expiry_index()
        raise("Not Implemented")

    @classmethod
    def load(opts, throttle_ms: int):
        instance = ZetaGroupMarkets()
        raise("Not implemented")

    def subscribe_market(self,market_index):
        if market_index >= len(self._markets):
            raise(f"Market Index {market_index} does not exist")
        self._subscribed_market_indexes.add(market_index)

    def unsubscribe_market(self, market_index):
        self._subscribed_market_indexes.remove(market_index)


    def products_per_expiry() -> int:
        return math.floor(len(self._markets.length), len(self._expiry_series))

class ExpirySeries():

    def __init__(self, expiry_index: int, active_ts: int, expiry_ts: int, dirty: bool, strikes_initialized: bool):
        self.expiry_index = expiry_index
        self.active_ts = active_ts
        self.expiry_ts = expiry_ts
        self.dirty = dirty
        self.strikes_initialized = strikes_initialized

    def is_live()-> bool:
        raise("To be implemented")

class Market:
    def __init__(
        self,
        market_index,
        expiry_index,
        kind,
        address,
        zeta_group,
        quote_vault,
        base_vault,
        serum_market,
    ):
        self._market_index = market_index
        self._expiry_index = expiry_index
        self._kind = kind
        self._address = address
        self._zeta_group = zeta_group
        self._quote_vault = quote_vault
        self._base_vault = base_vault
        self._serum_market = serum_market
        self._orderbook = {"bids": [], "asks": []}
        self._strike = 0

    @property
    def expiry_index(self):
        return self._expiry_index

    # TODO: Reinstate after adding market property to Exchange
    # def expiry_series():
    #     pass

    @property
    def kind(self):
        return self._kind

    @property
    def address(self):
        return self._address

    @property
    def market_index(self):
        return self.market_index

    @property
    def zeta_group(self):
        return self._zeta_group

    @property
    def quote_vault(self):
        return self._quote_vault

    @property
    def base_vault(self):
        return self._base_vault

    @property
    def serum_market(self):
        return self._serum_market

    @property
    def orderbook(self):
        return self._orderbook

    @property
    def strikes(self):
        return self.strikes

    def update_order_book(self):
        # self._bids = self._serum_market.load_bids(Exchange.provider.connection)
        # self._asks = self._serum_market.load_asks(Exchange.provider.connection)
        # orderbook_sides = [self._bids, self._asks]
        """
        for orderbook_side in orderbook_sides:
            descending = orderbook_side.is_bids ? True : False
            slab_items = list(orderbook_side._slab.items(descending))[0]
            key = slab_items.key
            quantity = slab_items.quantity
            price = orderbook_side.__get_price_from_slab(orderbook_side._slab)

            levels = []
            # Convert generator to key and quan
            descending = orderbook_side.slab
        """
        pass
