import atexit
import asyncio
from zetamarkets import constants
from network import Network
from pythclient.pythaccounts import PythPriceAccount, PythPriceStatus
from pythclient.solana import SolanaClient, SolanaPublicKey, SOLANA_DEVNET_HTTP_ENDPOINT, SOLANA_DEVNET_WS_ENDPOINT, SOLANA_TESTNET_HTTP_ENDPOINT, SOLANA_TESTNET_WS_ENDPOINT, SOLANA_MAINNET_HTTP_ENDPOINT, SOLANA_MAINNET_WS_ENDPOINT

class Oracle:
    def __init__(self, network, connection):
        self._network = network
        self._connection = connection
        self._subscription_ids = {}
        self._data = {}
        self._callback = None
        if self._network ==  Network.LOCALNET:
            self._solana_client = SolanaClient(endpoint=SOLANA_TESTNET_HTTP_ENDPOINT, ws_endpoint=SOLANA_TESTNET_WS_ENDPOINT)
        elif self._network == Network.DEVNET:
            self._solana_client = SolanaClient(endpoint=SOLANA_DEVNET_HTTP_ENDPOINT, ws_endpoint=SOLANA_DEVNET_WS_ENDPOINT)
        elif self._network == Network.MAINNET:
            self._solana_client = SolanaClient(endpoint=SOLANA_MAINNET_HTTP_ENDPOINT, ws_endpoint=SOLANA_MAINNET_WS_ENDPOINT)
        pyth_account_key = SolanaPublicKey(str(constants.PYTH_PRICE_FEEDS[self._network].get("SOL/USD")))
        self._price = PythPriceAccount(pyth_account_key, self._solana_client)
        # https://docs.python.org/3/library/atexit.html#atexit.register
        # atexit.register(lambda: asyncio.get_event_loop().run_until_complete(self._solana_client.close()))

    def get_available_price_feeds(self):
        return constants.PYTH_PRICE_FEEDS[self._network].keys()

    async def get_price(self):
        await self._price.update()
        price_status = self._price.aggregate_price_status
        if price_status == PythPriceStatus.TRADING:
            return self._price.aggregate_price
        else:
            print("Price is not valid now. Status is", price_status)
