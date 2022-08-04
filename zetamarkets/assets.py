from asyncio import constants
import enum

class Asset(enum.Enum):
    SOL = 0
    BTC = 1
    ETH = 2
    UNDEFINED = 255

from constants import MINTS

def assetToName(asset):
    if asset == Asset.SOL: return "SOL"
    elif asset == Asset.BTC: return "BTC"
    elif asset == Asset.ETH: return "ETH"
    elif asset == Asset.UNDEFINED: return "UNDEFINED"
    else: return "ERROR" #Invalid asset type

def nameToAsset(name):
    if name == "SOL": return Asset.SOL
    elif name == "BTC": return Asset.BTC
    elif name == "ETH": return Asset.ETH
    elif name == "UNDEFINED": return Asset.UNDEFINED
    else: return "ERROR" #Invalid input name

def allAssets():
    retAssets = []
    for asset in Asset:
        if isinstance(asset.value, int):
            retAssets.append(nameToAsset(asset.name))
    return asset

def isValidType(asset):
    return assetToName(asset) != "ERROR"

def isValidStr(assetStr):
    return nameToAsset(assetStr) != "ERROR"

def getAssetMint(asset):
    if assetToName(asset) != "ERROR":
        return MINTS[assetToName(asset)]
    return -1

def toProgramAsset(asset):
    if asset == Asset.SOL: return { "sol": {} }
    if asset == Asset.BTC: return { "btc": {} }
    if asset == Asset.ETH: return { "eth": {} }
    return "ERROR"

def fromProgramAsset(obj):
    if obj == { "sol": {} }: return Asset.SOL
    if obj == { "btc": {} }: return Asset.BTC
    if obj == { "eth": {} }: return Asset.ETH
    return "ERROR"