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


class ReferrerAccountJSON(typing.TypedDict):
    nonce: int
    has_alias: bool
    referrer: str
    pending_rewards: int
    claimed_rewards: int


@dataclass
class ReferrerAccount:
    discriminator: typing.ClassVar = b"0\x13\xa06L\xdcF\t"
    layout: typing.ClassVar = borsh.CStruct(
        "nonce" / borsh.U8,
        "has_alias" / borsh.Bool,
        "referrer" / BorshPubkey,
        "pending_rewards" / borsh.U64,
        "claimed_rewards" / borsh.U64,
    )
    nonce: int
    has_alias: bool
    referrer: PublicKey
    pending_rewards: int
    claimed_rewards: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: PublicKey,
        commitment: typing.Optional[Commitment] = None,
    ) -> typing.Optional["ReferrerAccount"]:
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
    ) -> typing.List[typing.Optional["ReferrerAccount"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["ReferrerAccount"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != PROGRAM_ID:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "ReferrerAccount":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = ReferrerAccount.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            nonce=dec.nonce,
            has_alias=dec.has_alias,
            referrer=dec.referrer,
            pending_rewards=dec.pending_rewards,
            claimed_rewards=dec.claimed_rewards,
        )

    def to_json(self) -> ReferrerAccountJSON:
        return {
            "nonce": self.nonce,
            "has_alias": self.has_alias,
            "referrer": str(self.referrer),
            "pending_rewards": self.pending_rewards,
            "claimed_rewards": self.claimed_rewards,
        }

    @classmethod
    def from_json(cls, obj: ReferrerAccountJSON) -> "ReferrerAccount":
        return cls(
            nonce=obj["nonce"],
            has_alias=obj["has_alias"],
            referrer=PublicKey(obj["referrer"]),
            pending_rewards=obj["pending_rewards"],
            claimed_rewards=obj["claimed_rewards"],
        )
