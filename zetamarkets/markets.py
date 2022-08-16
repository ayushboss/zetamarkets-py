import math
from time import sleep
from constants import NUM_STRIKES, PRODUCTS_PER_EXPIRY
import constants
from var_types import Kind
from assets import Asset
import utils
import var_types as types
from pyserum.market import Market as SerumMarket
from solana.rpc.api import Client
import network

class ZetaGroupMarkets:

    ## TODO: init the singleton, for now we list it as Exchange

    def __init__(self, asset):
        from exchange import Exchange
        self._expiry_series = [None] * len(Exchange.get_sub_exchange(self, asset)._zeta_group.expiry_series)
        self._markets = [None] * len(Exchange.get_sub_exchange(self, asset)._zeta_group.products)
        self._last_poll_timestamp = 0
        self._subscribed_market_indexes = set()
        self._asset = asset

    # @staticmethod
    # async def load(opts, throttle_ms):
    #     instance = ZetaGroupMarkets()
    #     products_per_expiry = math.floor(len(Exchange._zeta_group.products), len(Exchange.zeta_group.expiry_series))
    #     indexes = [i for i in range(ACTIVE_MARKETS)]
    #     for i in range(0, len(indexes), MARKET_LOAD_LIMIT):
    #         slice = indexes[i: i+ MARKET_LOAD_LIMIT]
    #         await asyncio.gather()
    #         # TODO: Port logic and figure out how to transfer promise.all

    #     instance.update_expiry_series()
    #     return instance

    async def load(self, asset: Asset, opts, throttle_ms: int):
        from exchange import Exchange
        instance = ZetaGroupMarkets(asset)
        sub_exchange = Exchange.get_sub_exchange(self, asset)

        products_per_expiry = PRODUCTS_PER_EXPIRY
        indexes = []
        for i in range(constants.ACTIVE_MARKETS):
            indexes.append(i)
        
        i = 0
        while i < len(indexes):
            slice = indexes[i:i+constants.MARKET_LOAD_LIMIT]
            j = 0
            for index in slice:
                market_addr = sub_exchange.zeta_group.products[index].market
                print(Exchange.network == network.Network.DEVNET)
                NETWORK_URL = "https://api.devnet.solana.com"

                connection = Client(NETWORK_URL, utils.default_commitment())
                print("market address")
                print(market_addr)
                serum_market: SerumMarket = SerumMarket.load(
                    connection,
                    market_addr,
                    constants.DEX_PID[Exchange.network],
                )
                
                print("mintcoming")
                print(serum_market.state.base_mint())
                print(serum_market.state.quote_mint())

                base_vault_addr, _base_vault_nonce = utils.get_zeta_vault(
                    Exchange.program_id,
                    serum_market.state.base_mint()
                )
                quote_vault_addr, _quote_vault_nonce = utils.get_zeta_vault(
                    Exchange.program_id,
                    serum_market.state.quote_mint()
                )

                expiry_index = math.floor(index/products_per_expiry)

                instance._markets[index] = Market(
                    asset, 
                    index, 
                    expiry_index, 
                    types.to_product_kind(sub_exchange.zeta_group.products[index].kind),
                    market_addr,
                    sub_exchange.zeta_group_address,
                    quote_vault_addr,
                    base_vault_addr,
                    serum_market
                )
                i+=1
                j+=1
            print(throttle_ms)
            sleep(throttle_ms*1000)
        instance.update_expiry_series()
        return instance

    def update_expiry_series(self):
        from exchange import Exchange
        subex = Exchange.get_sub_exchange(self, self._asset)
        for i in range(len(subex._zeta_group.products)):
            self._markets[i].update_strike()
        self._front_expiry_index = subex._zeta_group.front_expiry_index
        for j in range(len(subex._zeta_group.expiry_series)):
            strikes_initialized = self._markets[j * self.products_per_expiry()]._strike is not None
            self._expiry_series[j] = ExpirySeries(j,
                                                  int(subex._zeta_group.expiry_series[j].active_ts),
                                                  int(subex._zeta_group.expiry_series[j].expiry_ts),
                                                  subex._zeta_group.expiry_series[j].dirty,
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

    # @classmethod
    # def load(asset: Asset, opts, throttle_ms: int):
    #     instance = ZetaGroupMarkets()
    #     instance._asset = asset

    #     raise("Not implemented")

    def subscribe_market(self,market_index):
        if market_index >= len(self._markets):
            raise(f"Market Index {market_index} does not exist")
        self._subscribed_market_indexes.add(market_index)

    def unsubscribe_market(self, market_index):
        self._subscribed_market_indexes.remove(market_index)


    def products_per_expiry(self) -> int:
        return math.floor(len(self._markets)/len(self._expiry_series))

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
            return markets[NUM_STRIKES, 2 * NUM_STRIKES]
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
        return None if len(markets) == 0 else markets[0]



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
        asset,
        market_index,
        expiry_index,
        kind,
        address,
        zeta_group,
        quote_vault,
        base_vault,
        serum_market,
    ):
        self._asset = asset
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
        from exchange import Exchange
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
    
    def update_strike(self):
        from exchange import Exchange
        strike = Exchange.get_sub_exchange(self, self._asset).zeta_group.products[self._market_index].strike
        if not strike.is_set:
            self._strike = None
        else:
            self._strike = strike.value