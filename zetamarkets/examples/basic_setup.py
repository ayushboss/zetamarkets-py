import asyncio
import os
import json
import array as arr
import solana
from solana.keypair import Keypair
from solana.rpc.api import Client
from typing import Dict
from zetamarkets import utils
from zetamarkets.exchange import Exchange
from solana.publickey import PublicKey
from solana.rpc.async_api import AsyncClient

keypair = Keypair()


# print(str(json.loads(test)))
# private_key = keypair.from_secret_key(str(test[:32]))

SERVER_URL = "https://server.zeta.markets"
NETWORK_URL = "https://api.devnet.solana.com"

# // Starts a solana web3 connection to an RPC endpoint
connection = Client(NETWORK_URL, utils.default_commitment())

# // Airdrop some SOL to your wallet
wallet = PublicKey("8LpEYmLf7LUcd3aEKNSmNZyYmzD8osbacK4Qb4WGTv3o")
#conn = connection.request_airdrop(wallet, 100000000)
#print(conn)


mint_auth = solana.publickey.PublicKey("SRMuApVNdxXokk5GT7XD5cUUgXMBCoAz2LHeuAoKWRt")

# Exchange.load(mint_auth, "", "", "", "", "")

import httpx
import json

# with httpx.Client() as client:
#     res = client.post(
#        f"{SERVER_URL}/faucet/USDC",
#         data=
#             {
#                 "key": str(wallet),
#                 "amount": 10000,
#             }
#         ,
#         headers={"Content-Type": "application/json"},
#     )
#     print(res)
PROGRAM_ID = "BG3oRikW8d16YjUEmX3ZxHm9SiJzrGtMhsSR8aCw1Cd7"
# Fill this ins
conn = AsyncClient(NETWORK_URL)
print(utils.default_commitment())
Exchange.load(PROGRAM_ID, "devnet", conn, utils.default_commitment(), None, 0)


print("stuff")
# // USDC faucet - Mint $10,000 USDC (Note USDC is fake on devnet)
# async def main():

#     await get_vault()
# async with httpx.AsyncClient() as client:
#     res = await client.post(
#         f"{SERVER_URL}/faucet/USDC",
#         data=json.dumps(
#             {
#                 "key": str(keypair.public_key),
#                 "amount": 10000,
#             }
#         ),
#         headers={"Content-Type": "application/json"},
#     )


# asyncio.run(main())
# // Loads the SDK exchange singleton. This can take up to 10 seconds...
# await Exchange.load(
#   PROGRAM_ID,
#   Network.DEVNET,
#   connection,
#   utils.defaultCommitment(),
#   undefined, // Exchange wallet can be ignored for normal clients.
#   0, // ThrottleMs - increase if you are running into rate limit issues on startup.
#   undefined // Callback - See below for more details.
# );
