from zetamarkets import constants


class Oracle:
    def __init__(self, network, connection):
        self._network = network
        self._connection = connection
        self._subscription_ids = {}
        self._data = {}
        self._callback = None

    def get_available_price_feeds(self):
        return constants.PYTH_PRICE_FEEDS[self._network].keys()

    def get_price(self, feed):
        if not feed in self._data:
            return None
        return self._data.get(feed)

    def fetch_price(self, oracle_key):
        # TODO parse account_info.data
        account_info = self._connection.get_account_info(oracle_key)
        price_data = account_info.data
        return price_data.price

    def subscribe_price_feeds(self, callback):
        if self._callback is not None:
            raise ("Oracle price feeds already subscribed to!")
        self._callback = callback
        feeds = constants.PYTH_PRICE_FEEDS[self._network].keys()
        for i in range(len(feeds)):
            feed = feeds[i]
            print(f"Oracle subscribing to feed {feed}")
            price_address = constants.PYTH_PRICE_FEEDS[self._network][feed]

            def on_account_change_fn(account_info, _context):
                # TODO parse price data
                price_data = account_info.data
                curr_price = self._data.get(feed)
                if curr_price is not None and curr_price.price == price_data.price:
                    return
                oracle_data = {"feed": feed, "price": price_data.price}
                self._data[feed] = oracle_data
                self._callback(oracle_data)
                # Convert logic
                # Exchange.provider.connection.commitment

            # subscription_id = self._connection.on_account_change(price_address, on_account_change_fn)

            # self._subscription_ids[feed] = subscription_id
            # account_info =  self._connection.get_account_info(price_address)
            # price_data = parse_pyth_data(account_info.data);
            # oracle_data = {"feed": feed, "price": price_data.price}
            self._data[feed] = oracle_data
