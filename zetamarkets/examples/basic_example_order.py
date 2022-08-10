import sys
sys.path.append("../")

from newclient import Client as ZetaClient
from exchange import Exchange
from network import Network
import var_types as types
import assets
import utils


from anchorpy import Wallet
from solana.publickey import PublicKey
from solana.rpc.api import Client
from solana.rpc.async_api import AsyncClient
from solana.keypair import Keypair

keypair = Keypair()

SERVER_URL = "https://server.zeta.markets"
NETWORK_URL = "https://api.devnet.solana.com"

connection = Client(NETWORK_URL, utils.default_commitment())

wallet = PublicKey("8LpEYmLf7LUcd3aEKNSmNZyYmzD8osbacK4Qb4WGTv3o")

connection.request_airdrop(wallet, 100000000)
mint_auth = PublicKey("SRMuApVNdxXokk5GT7XD5cUUgXMBCoAz2LHeuAoKWRt")

PROGRAM_ID = PublicKey("BG3oRikW8d16YjUEmX3ZxHm9SiJzrGtMhsSR8aCw1Cd7")
# Fill this ins
conn = AsyncClient(NETWORK_URL)

STARTING_BALANCE = 5000

def cb(asset: assets.Asset, event, data):
    print("Asset: " + str(asset))

async def main():
    exc = Exchange("","","","")
    assets_in_exchange = [assets.Asset.SOL, assets.Asset.BTC]
    await exc.load(PROGRAM_ID, "devnet", conn, utils.default_commitment(), wallet, 0, assets_in_exchange, cb)

    cl = await ZetaClient.load(conn, wallet, utils.default_commitment(), cb, 0)
    deposit_transaction = await cl.deposit(assets.Asset.BTC, utils.convert_decimal_to_native_integer(STARTING_BALANCE))

    print(deposit_transaction)
