from enum import Enum

class Network(Enum):
    LOCALNET = "localnet"
    DEVNET = "devnet"
    MAINNET = "mainnet"

def toNetwork(networkStr):
    if networkStr == "localnet": return Network.LOCALNET
    if networkStr == "devnet": return Network.DEVNET
    if networkStr == "mainnet": return Network.MAINNET