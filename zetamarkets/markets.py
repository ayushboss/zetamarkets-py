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
