import asyncio
import os
import json
import array as arr
import solana
from solana.keypair import Keypair
from solana.rpc.api import Client
from typing import Dict
from zetamarkets.exchange import Exchange


keypair = Keypair()


# print(str(json.loads(test)))
# private_key = keypair.from_secret_key(str(test[:32]))

SERVER_URL = "https://server.zeta.markets"
NETWORK_URL = "https://api.devnet.solana.com"

# // Starts a solana web3 connection to an RPC endpoint
connection = Client(NETWORK_URL, default_commitment())

# // Airdrop some SOL to your wallet
conn = connection.request_airdrop(keypair.public_key, 100000000)
print(conn)


mint_auth = solana.publickey.PublicKey("SRMuApVNdxXokk5GT7XD5cUUgXMBCoAz2LHeuAoKWRt")
Exchange.load(mint_auth, "", "", "", "", "")


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
