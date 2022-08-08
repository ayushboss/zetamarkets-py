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


class SpreadAccountJSON(typing.TypedDict):
    authority: str
    nonce: int
    balance: int
    series_expiry: list[int]
    positions: list[types.position.PositionJSON]
    positions_padding: list[types.position.PositionJSON]
    asset: types.asset.AssetJSON
    padding: list[int]


@dataclass
class SpreadAccount:
    discriminator: typing.ClassVar = b"9\x82\xfc\x88\xa7\xb1/\xa2"
    layout: typing.ClassVar = borsh.CStruct(
        "authority" / BorshPubkey,
        "nonce" / borsh.U8,
        "balance" / borsh.U64,
        "series_expiry" / borsh.U64[6],
        "positions" / types.position.Position.layout[46],
        "positions_padding" / types.position.Position.layout[92],
        "asset" / types.asset.layout,
        "padding" / borsh.U8[262],
    )
    authority: PublicKey
    nonce: int
    balance: int
    series_expiry: list[int]
    positions: list[types.position.Position]
    positions_padding: list[types.position.Position]
    asset: types.asset.AssetKind
    padding: list[int]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: PublicKey,
        commitment: typing.Optional[Commitment] = None,
    ) -> typing.Optional["SpreadAccount"]:
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
    ) -> typing.List[typing.Optional["SpreadAccount"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["SpreadAccount"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != PROGRAM_ID:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "SpreadAccount":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = SpreadAccount.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            authority=dec.authority,
            nonce=dec.nonce,
            balance=dec.balance,
            series_expiry=dec.series_expiry,
            positions=list(
                map(
                    lambda item: types.position.Position.from_decoded(item),
                    dec.positions,
                )
            ),
            positions_padding=list(
                map(
                    lambda item: types.position.Position.from_decoded(item),
                    dec.positions_padding,
                )
            ),
            asset=types.asset.from_decoded(dec.asset),
            padding=dec.padding,
        )

    def to_json(self) -> SpreadAccountJSON:
        return {
            "authority": str(self.authority),
            "nonce": self.nonce,
            "balance": self.balance,
            "series_expiry": self.series_expiry,
            "positions": list(map(lambda item: item.to_json(), self.positions)),
            "positions_padding": list(
                map(lambda item: item.to_json(), self.positions_padding)
            ),
            "asset": self.asset.to_json(),
            "padding": self.padding,
        }

    @classmethod
    def from_json(cls, obj: SpreadAccountJSON) -> "SpreadAccount":
        return cls(
            authority=PublicKey(obj["authority"]),
            nonce=obj["nonce"],
            balance=obj["balance"],
            series_expiry=obj["series_expiry"],
            positions=list(
                map(
                    lambda item: types.position.Position.from_json(item),
                    obj["positions"],
                )
            ),
            positions_padding=list(
                map(
                    lambda item: types.position.Position.from_json(item),
                    obj["positions_padding"],
                )
            ),
            asset=types.asset.from_json(obj["asset"]),
            padding=obj["padding"],
        )
