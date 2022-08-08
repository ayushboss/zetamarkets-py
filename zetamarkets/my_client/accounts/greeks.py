import typing
from dataclasses import dataclass
from base64 import b64decode
from solana.publickey import PublicKey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
import borsh_construct as borsh
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from anchorpy.borsh_extension import BorshPubkey
from ..program_id import PROGRAM_ID
from .. import types


class GreeksJSON(typing.TypedDict):
    nonce: int
    mark_prices: list[int]
    mark_prices_padding: list[int]
    product_greeks: list[types.product_greeks.ProductGreeksJSON]
    product_greeks_padding: list[types.product_greeks.ProductGreeksJSON]
    update_timestamp: list[int]
    update_timestamp_padding: list[int]
    retreat_expiration_timestamp: list[int]
    retreat_expiration_timestamp_padding: list[int]
    interest_rate: list[int]
    interest_rate_padding: list[int]
    nodes: list[int]
    volatility: list[int]
    volatility_padding: list[int]
    node_keys: list[str]
    halt_force_pricing: list[bool]
    padding: list[int]


@dataclass
class Greeks:
    discriminator: typing.ClassVar = b"\xf7\xd5\xaa\x9a+\xf3\x92\xfe"
    layout: typing.ClassVar = borsh.CStruct(
        "nonce" / borsh.U8,
        "mark_prices" / borsh.U64[46],
        "mark_prices_padding" / borsh.U64[92],
        "product_greeks" / types.product_greeks.ProductGreeks.layout[22],
        "product_greeks_padding" / types.product_greeks.ProductGreeks.layout[44],
        "update_timestamp" / borsh.U64[2],
        "update_timestamp_padding" / borsh.U64[4],
        "retreat_expiration_timestamp" / borsh.U64[2],
        "retreat_expiration_timestamp_padding" / borsh.U64[4],
        "interest_rate" / borsh.I64[2],
        "interest_rate_padding" / borsh.I64[4],
        "nodes" / borsh.U64[5],
        "volatility" / borsh.U64[10],
        "volatility_padding" / borsh.U64[20],
        "node_keys" / BorshPubkey[138],
        "halt_force_pricing" / borsh.Bool[6],
        "padding" / borsh.U8[1641],
    )
    nonce: int
    mark_prices: list[int]
    mark_prices_padding: list[int]
    product_greeks: list[types.product_greeks.ProductGreeks]
    product_greeks_padding: list[types.product_greeks.ProductGreeks]
    update_timestamp: list[int]
    update_timestamp_padding: list[int]
    retreat_expiration_timestamp: list[int]
    retreat_expiration_timestamp_padding: list[int]
    interest_rate: list[int]
    interest_rate_padding: list[int]
    nodes: list[int]
    volatility: list[int]
    volatility_padding: list[int]
    node_keys: list[PublicKey]
    halt_force_pricing: list[bool]
    padding: list[int]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: PublicKey,
        commitment: typing.Optional[Commitment] = None,
    ) -> typing.Optional["Greeks"]:
        resp = await conn.get_account_info(address, commitment=commitment)
        info = resp["result"]["value"]
        if info is None:
            return None
        if info["owner"] != str(PROGRAM_ID):
            raise ValueError("Account does not belong to this program")
        bytes_data = b64decode(info["data"][0])
        return cls.decode(bytes_data)

    @classmethod
    async def fetch_multiple(
        cls,
        conn: AsyncClient,
        addresses: list[PublicKey],
        commitment: typing.Optional[Commitment] = None,
    ) -> typing.List[typing.Optional["Greeks"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["Greeks"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != PROGRAM_ID:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "Greeks":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = Greeks.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            nonce=dec.nonce,
            mark_prices=dec.mark_prices,
            mark_prices_padding=dec.mark_prices_padding,
            product_greeks=list(
                map(
                    lambda item: types.product_greeks.ProductGreeks.from_decoded(item),
                    dec.product_greeks,
                )
            ),
            product_greeks_padding=list(
                map(
                    lambda item: types.product_greeks.ProductGreeks.from_decoded(item),
                    dec.product_greeks_padding,
                )
            ),
            update_timestamp=dec.update_timestamp,
            update_timestamp_padding=dec.update_timestamp_padding,
            retreat_expiration_timestamp=dec.retreat_expiration_timestamp,
            retreat_expiration_timestamp_padding=dec.retreat_expiration_timestamp_padding,
            interest_rate=dec.interest_rate,
            interest_rate_padding=dec.interest_rate_padding,
            nodes=dec.nodes,
            volatility=dec.volatility,
            volatility_padding=dec.volatility_padding,
            node_keys=dec.node_keys,
            halt_force_pricing=dec.halt_force_pricing,
            padding=dec.padding,
        )

    def to_json(self) -> GreeksJSON:
        return {
            "nonce": self.nonce,
            "mark_prices": self.mark_prices,
            "mark_prices_padding": self.mark_prices_padding,
            "product_greeks": list(
                map(lambda item: item.to_json(), self.product_greeks)
            ),
            "product_greeks_padding": list(
                map(lambda item: item.to_json(), self.product_greeks_padding)
            ),
            "update_timestamp": self.update_timestamp,
            "update_timestamp_padding": self.update_timestamp_padding,
            "retreat_expiration_timestamp": self.retreat_expiration_timestamp,
            "retreat_expiration_timestamp_padding": self.retreat_expiration_timestamp_padding,
            "interest_rate": self.interest_rate,
            "interest_rate_padding": self.interest_rate_padding,
            "nodes": self.nodes,
            "volatility": self.volatility,
            "volatility_padding": self.volatility_padding,
            "node_keys": list(map(lambda item: str(item), self.node_keys)),
            "halt_force_pricing": self.halt_force_pricing,
            "padding": self.padding,
        }

    @classmethod
    def from_json(cls, obj: GreeksJSON) -> "Greeks":
        return cls(
            nonce=obj["nonce"],
            mark_prices=obj["mark_prices"],
            mark_prices_padding=obj["mark_prices_padding"],
            product_greeks=list(
                map(
                    lambda item: types.product_greeks.ProductGreeks.from_json(item),
                    obj["product_greeks"],
                )
            ),
            product_greeks_padding=list(
                map(
                    lambda item: types.product_greeks.ProductGreeks.from_json(item),
                    obj["product_greeks_padding"],
                )
            ),
            update_timestamp=obj["update_timestamp"],
            update_timestamp_padding=obj["update_timestamp_padding"],
            retreat_expiration_timestamp=obj["retreat_expiration_timestamp"],
            retreat_expiration_timestamp_padding=obj[
                "retreat_expiration_timestamp_padding"
            ],
            interest_rate=obj["interest_rate"],
            interest_rate_padding=obj["interest_rate_padding"],
            nodes=obj["nodes"],
            volatility=obj["volatility"],
            volatility_padding=obj["volatility_padding"],
            node_keys=list(map(lambda item: PublicKey(item), obj["node_keys"])),
            halt_force_pricing=obj["halt_force_pricing"],
            padding=obj["padding"],
        )
