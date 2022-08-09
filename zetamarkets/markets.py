import math
from zetamarkets.constants import NUM_STRIKES
from zetamarkets.var_types import Kind
from exchange import Exchange

class ZetaGroupMarkets:

    ## TODO: init the singleton, for now we list it as Exchange

    def __init__(self):
        self._expiry_series = [None] * len(Exchange._zeta_group.expiry_series)
        self._markets = [None] * len(Exchange._zeta_group.products)
        self._last_poll_timestamp = 0
        self._subscribed_market_indexes = set()

    @staticmethod
    async def load(opts, throttle_ms):
        instance = ZetaGroupMarkets()
        products_per_expiry = math.floor(len(Exchange._zeta_group.products), len(Exchange.zeta_group.expiry_series))
        indexes = [i for i in range(ACTIVE_MARKETS)]
        for i in range(0, len(indexes), MARKET_LOAD_LIMIT):
            slice = indexes[i: i+ MARKET_LOAD_LIMIT]
            await asyncio.gather()
            # TODO: Port logic and figure out how to transfer promise.all

        instance.update_expiry_series()
        return instance

    def update_expiry_series(self):
        for i in range(len(Exchange._zeta_group.products)):
            self._markets[i].update_strike()
        self._front_expiry_index = Exchange._zeta_group.front_expiry_index
        for j in range(len(Exchange._zeta_group.expiry_series)):
            strikes_initialized = self._markets[j * self.products_per_expiry()].strike is not None
            self._expiry_series[j] = ExpirySeries(j,
                                                  int(Exchange._zeta_group.expiry_series[j].active_ts),
                                                  int(Exchange._zeta_group.expiry_series[j].expiry_ts),
                                                  Exchange._zeta_group.expiry_series[j].dirty,
                                                  strikes_initialized)

    def get_market(self, market):
        index = self.get_market_index(market)
        return self._markets[index]

    def get_market_index(market):
        # TODO: Implement this
        raise("Get market is not implemented")

    def get_tradeable_expiry_indices(self):
        result = []
        for index, expiry_series in enumerate(self._expiry_series):
            if expiry_series.is_live():
                result.append(index)
        return result


    @property
    def front_expiry_index(self):
        return self._front_expiry_index

    @property
    def expiry_series(self):
        return self._expiry_series

    @property
    def markets(self):
        return self._markets

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

    def get_markets_by_expiry_index(self, expiry_index: int):
        head = expiry_index * self.products_per_expiry_index()
        return self._markets[head: head+ self.products_per_expiry()]

    def get_options_market_by_expiry_index(self, expiry_index: int, kind):
        """
        Returns the options market given an expiry index and options kind.
        """
        markets = self.get_markets_by_expiry_index(expiry_index)
        if kind == Kind.CALL:
            return markets[NUM_STRIKES]
        elif kind == Kind.PUT:
            return markets[NUM_STRIKES, 2 * MARKET_STRIKES]
        else:
            raise("Options market kind not supported, must be CALL or PUT")

    def get_futures_market_by_expiry_index(self, expiry_index: int):
        markets = self.get_markets_by_expiry_index(expiry_index)
        market = markets[len(markets) - 1]
        if market.kind != Kind.FUTURE:
            raise("Futures market kind error")
        return market

    def get_market_by_expiry_kind_strike(self, expiry_index, kind, strike=None):
        markets = self.get_markets_by_expiry_index(expiry_index)
        if kind == kind.CALL or kind == kind.PUT:
            if strike == None:
                raise("Strike must be specified for options markets")
            markets_kind = self.get_options_market_by_expiry_index(expiry_index, kind)
        elif kind == kind.FUTURE:
            return self.get_futures_market_by_expiry_index(expiry_index)
        else:
            raise("Only CALL, PUT, FUTURE kinds are supported")
        market = list(filter(lambda x: x.strike == strike, markets_kind))
        return None if len(markets) == 0 else: markets[0]



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

        [self._bids, self._asks] = asyncio.gather(self._serum_market.load_bids(Exchange.provider.connection),
                                                 self._serum_market.load_asks(Exchange.provider.connection))

        # TO fill
        # map([self._bids, self._asks])
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
