from zetamarkets import exchange, utils, network
from solana.rpc.api import Client
from solana.keypair import Keypair

SERVER_URL = "https://server.zeta.markets"
NETWORK_URL = "https://api.devnet.solana.com"
PROGRAM_ID = "BG3oRikW8d16YjUEmX3ZxHm9SiJzrGtMhsSR8aCw1Cd7"
netw = network.Network.LOCALNET.value
# // Starts a solana web3 connection to an RPC endpoint
connection = Client(NETWORK_URL, utils.default_commitment())

wallet = Keypair()


if __name__ == "__main__":
    exch = exchange.Exchange(PROGRAM_ID, str(netw), connection, wallet)

    print(exch.oracle.get_available_price_feeds())
    price = exch.oracle.get_price("SOL/USD")
    print(price)
