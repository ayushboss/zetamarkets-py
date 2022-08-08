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


class StateJSON(typing.TypedDict):
    admin: str
    state_nonce: int
    serum_nonce: int
    mint_auth_nonce: int
    num_underlyings: int
    expiry_interval_seconds: int
    new_expiry_threshold_seconds: int
    strike_initialization_threshold_seconds: int
    pricing_frequency_seconds: int
    liquidator_liquidation_percentage: int
    insurance_vault_liquidation_percentage: int
    native_d1_trade_fee_percentage: int
    native_d1_underlying_fee_percentage: int
    native_whitelist_underlying_fee_percentage: int
    native_deposit_limit: int
    expiration_threshold_seconds: int
    position_movement_fee_bps: int
    margin_concession_percentage: int
    treasury_wallet_nonce: int
    native_option_trade_fee_percentage: int
    native_option_underlying_fee_percentage: int
    padding: list[int]


@dataclass
class State:
    discriminator: typing.ClassVar = b"\xd8\x92k^hK\xb6\xb1"
    layout: typing.ClassVar = borsh.CStruct(
        "admin" / BorshPubkey,
        "state_nonce" / borsh.U8,
        "serum_nonce" / borsh.U8,
        "mint_auth_nonce" / borsh.U8,
        "num_underlyings" / borsh.U8,
        "expiry_interval_seconds" / borsh.U32,
        "new_expiry_threshold_seconds" / borsh.U32,
        "strike_initialization_threshold_seconds" / borsh.U32,
        "pricing_frequency_seconds" / borsh.U32,
        "liquidator_liquidation_percentage" / borsh.U32,
        "insurance_vault_liquidation_percentage" / borsh.U32,
        "native_d1_trade_fee_percentage" / borsh.U64,
        "native_d1_underlying_fee_percentage" / borsh.U64,
        "native_whitelist_underlying_fee_percentage" / borsh.U64,
        "native_deposit_limit" / borsh.U64,
        "expiration_threshold_seconds" / borsh.U32,
        "position_movement_fee_bps" / borsh.U8,
        "margin_concession_percentage" / borsh.U8,
        "treasury_wallet_nonce" / borsh.U8,
        "native_option_trade_fee_percentage" / borsh.U64,
        "native_option_underlying_fee_percentage" / borsh.U64,
        "padding" / borsh.U8[140],
    )
    admin: PublicKey
    state_nonce: int
    serum_nonce: int
    mint_auth_nonce: int
    num_underlyings: int
    expiry_interval_seconds: int
    new_expiry_threshold_seconds: int
    strike_initialization_threshold_seconds: int
    pricing_frequency_seconds: int
    liquidator_liquidation_percentage: int
    insurance_vault_liquidation_percentage: int
    native_d1_trade_fee_percentage: int
    native_d1_underlying_fee_percentage: int
    native_whitelist_underlying_fee_percentage: int
    native_deposit_limit: int
    expiration_threshold_seconds: int
    position_movement_fee_bps: int
    margin_concession_percentage: int
    treasury_wallet_nonce: int
    native_option_trade_fee_percentage: int
    native_option_underlying_fee_percentage: int
    padding: list[int]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: PublicKey,
        commitment: typing.Optional[Commitment] = None,
    ) -> typing.Optional["State"]:
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
    ) -> typing.List[typing.Optional["State"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["State"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != PROGRAM_ID:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "State":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = State.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            admin=dec.admin,
            state_nonce=dec.state_nonce,
            serum_nonce=dec.serum_nonce,
            mint_auth_nonce=dec.mint_auth_nonce,
            num_underlyings=dec.num_underlyings,
            expiry_interval_seconds=dec.expiry_interval_seconds,
            new_expiry_threshold_seconds=dec.new_expiry_threshold_seconds,
            strike_initialization_threshold_seconds=dec.strike_initialization_threshold_seconds,
            pricing_frequency_seconds=dec.pricing_frequency_seconds,
            liquidator_liquidation_percentage=dec.liquidator_liquidation_percentage,
            insurance_vault_liquidation_percentage=dec.insurance_vault_liquidation_percentage,
            native_d1_trade_fee_percentage=dec.native_d1_trade_fee_percentage,
            native_d1_underlying_fee_percentage=dec.native_d1_underlying_fee_percentage,
            native_whitelist_underlying_fee_percentage=dec.native_whitelist_underlying_fee_percentage,
            native_deposit_limit=dec.native_deposit_limit,
            expiration_threshold_seconds=dec.expiration_threshold_seconds,
            position_movement_fee_bps=dec.position_movement_fee_bps,
            margin_concession_percentage=dec.margin_concession_percentage,
            treasury_wallet_nonce=dec.treasury_wallet_nonce,
            native_option_trade_fee_percentage=dec.native_option_trade_fee_percentage,
            native_option_underlying_fee_percentage=dec.native_option_underlying_fee_percentage,
            padding=dec.padding,
        )

    def to_json(self) -> StateJSON:
        return {
            "admin": str(self.admin),
            "state_nonce": self.state_nonce,
            "serum_nonce": self.serum_nonce,
            "mint_auth_nonce": self.mint_auth_nonce,
            "num_underlyings": self.num_underlyings,
            "expiry_interval_seconds": self.expiry_interval_seconds,
            "new_expiry_threshold_seconds": self.new_expiry_threshold_seconds,
            "strike_initialization_threshold_seconds": self.strike_initialization_threshold_seconds,
            "pricing_frequency_seconds": self.pricing_frequency_seconds,
            "liquidator_liquidation_percentage": self.liquidator_liquidation_percentage,
            "insurance_vault_liquidation_percentage": self.insurance_vault_liquidation_percentage,
            "native_d1_trade_fee_percentage": self.native_d1_trade_fee_percentage,
            "native_d1_underlying_fee_percentage": self.native_d1_underlying_fee_percentage,
            "native_whitelist_underlying_fee_percentage": self.native_whitelist_underlying_fee_percentage,
            "native_deposit_limit": self.native_deposit_limit,
            "expiration_threshold_seconds": self.expiration_threshold_seconds,
            "position_movement_fee_bps": self.position_movement_fee_bps,
            "margin_concession_percentage": self.margin_concession_percentage,
            "treasury_wallet_nonce": self.treasury_wallet_nonce,
            "native_option_trade_fee_percentage": self.native_option_trade_fee_percentage,
            "native_option_underlying_fee_percentage": self.native_option_underlying_fee_percentage,
            "padding": self.padding,
        }

    @classmethod
    def from_json(cls, obj: StateJSON) -> "State":
        return cls(
            admin=PublicKey(obj["admin"]),
            state_nonce=obj["state_nonce"],
            serum_nonce=obj["serum_nonce"],
            mint_auth_nonce=obj["mint_auth_nonce"],
            num_underlyings=obj["num_underlyings"],
            expiry_interval_seconds=obj["expiry_interval_seconds"],
            new_expiry_threshold_seconds=obj["new_expiry_threshold_seconds"],
            strike_initialization_threshold_seconds=obj[
                "strike_initialization_threshold_seconds"
            ],
            pricing_frequency_seconds=obj["pricing_frequency_seconds"],
            liquidator_liquidation_percentage=obj["liquidator_liquidation_percentage"],
            insurance_vault_liquidation_percentage=obj[
                "insurance_vault_liquidation_percentage"
            ],
            native_d1_trade_fee_percentage=obj["native_d1_trade_fee_percentage"],
            native_d1_underlying_fee_percentage=obj[
                "native_d1_underlying_fee_percentage"
            ],
            native_whitelist_underlying_fee_percentage=obj[
                "native_whitelist_underlying_fee_percentage"
            ],
            native_deposit_limit=obj["native_deposit_limit"],
            expiration_threshold_seconds=obj["expiration_threshold_seconds"],
            position_movement_fee_bps=obj["position_movement_fee_bps"],
            margin_concession_percentage=obj["margin_concession_percentage"],
            treasury_wallet_nonce=obj["treasury_wallet_nonce"],
            native_option_trade_fee_percentage=obj[
                "native_option_trade_fee_percentage"
            ],
            native_option_underlying_fee_percentage=obj[
                "native_option_underlying_fee_percentage"
            ],
            padding=obj["padding"],
        )
