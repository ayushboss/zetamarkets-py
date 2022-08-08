from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class UpdateStateArgsJSON(typing.TypedDict):
    expiry_interval_seconds: int
    new_expiry_threshold_seconds: int
    strike_initialization_threshold_seconds: int
    pricing_frequency_seconds: int
    liquidator_liquidation_percentage: int
    insurance_vault_liquidation_percentage: int
    native_d1_trade_fee_percentage: int
    native_d1_underlying_fee_percentage: int
    native_option_trade_fee_percentage: int
    native_option_underlying_fee_percentage: int
    native_whitelist_underlying_fee_percentage: int
    native_deposit_limit: int
    expiration_threshold_seconds: int
    position_movement_fee_bps: int
    margin_concession_percentage: int


@dataclass
class UpdateStateArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "expiry_interval_seconds" / borsh.U32,
        "new_expiry_threshold_seconds" / borsh.U32,
        "strike_initialization_threshold_seconds" / borsh.U32,
        "pricing_frequency_seconds" / borsh.U32,
        "liquidator_liquidation_percentage" / borsh.U32,
        "insurance_vault_liquidation_percentage" / borsh.U32,
        "native_d1_trade_fee_percentage" / borsh.U64,
        "native_d1_underlying_fee_percentage" / borsh.U64,
        "native_option_trade_fee_percentage" / borsh.U64,
        "native_option_underlying_fee_percentage" / borsh.U64,
        "native_whitelist_underlying_fee_percentage" / borsh.U64,
        "native_deposit_limit" / borsh.U64,
        "expiration_threshold_seconds" / borsh.U32,
        "position_movement_fee_bps" / borsh.U8,
        "margin_concession_percentage" / borsh.U8,
    )
    expiry_interval_seconds: int
    new_expiry_threshold_seconds: int
    strike_initialization_threshold_seconds: int
    pricing_frequency_seconds: int
    liquidator_liquidation_percentage: int
    insurance_vault_liquidation_percentage: int
    native_d1_trade_fee_percentage: int
    native_d1_underlying_fee_percentage: int
    native_option_trade_fee_percentage: int
    native_option_underlying_fee_percentage: int
    native_whitelist_underlying_fee_percentage: int
    native_deposit_limit: int
    expiration_threshold_seconds: int
    position_movement_fee_bps: int
    margin_concession_percentage: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "UpdateStateArgs":
        return cls(
            expiry_interval_seconds=obj.expiry_interval_seconds,
            new_expiry_threshold_seconds=obj.new_expiry_threshold_seconds,
            strike_initialization_threshold_seconds=obj.strike_initialization_threshold_seconds,
            pricing_frequency_seconds=obj.pricing_frequency_seconds,
            liquidator_liquidation_percentage=obj.liquidator_liquidation_percentage,
            insurance_vault_liquidation_percentage=obj.insurance_vault_liquidation_percentage,
            native_d1_trade_fee_percentage=obj.native_d1_trade_fee_percentage,
            native_d1_underlying_fee_percentage=obj.native_d1_underlying_fee_percentage,
            native_option_trade_fee_percentage=obj.native_option_trade_fee_percentage,
            native_option_underlying_fee_percentage=obj.native_option_underlying_fee_percentage,
            native_whitelist_underlying_fee_percentage=obj.native_whitelist_underlying_fee_percentage,
            native_deposit_limit=obj.native_deposit_limit,
            expiration_threshold_seconds=obj.expiration_threshold_seconds,
            position_movement_fee_bps=obj.position_movement_fee_bps,
            margin_concession_percentage=obj.margin_concession_percentage,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "expiry_interval_seconds": self.expiry_interval_seconds,
            "new_expiry_threshold_seconds": self.new_expiry_threshold_seconds,
            "strike_initialization_threshold_seconds": self.strike_initialization_threshold_seconds,
            "pricing_frequency_seconds": self.pricing_frequency_seconds,
            "liquidator_liquidation_percentage": self.liquidator_liquidation_percentage,
            "insurance_vault_liquidation_percentage": self.insurance_vault_liquidation_percentage,
            "native_d1_trade_fee_percentage": self.native_d1_trade_fee_percentage,
            "native_d1_underlying_fee_percentage": self.native_d1_underlying_fee_percentage,
            "native_option_trade_fee_percentage": self.native_option_trade_fee_percentage,
            "native_option_underlying_fee_percentage": self.native_option_underlying_fee_percentage,
            "native_whitelist_underlying_fee_percentage": self.native_whitelist_underlying_fee_percentage,
            "native_deposit_limit": self.native_deposit_limit,
            "expiration_threshold_seconds": self.expiration_threshold_seconds,
            "position_movement_fee_bps": self.position_movement_fee_bps,
            "margin_concession_percentage": self.margin_concession_percentage,
        }

    def to_json(self) -> UpdateStateArgsJSON:
        return {
            "expiry_interval_seconds": self.expiry_interval_seconds,
            "new_expiry_threshold_seconds": self.new_expiry_threshold_seconds,
            "strike_initialization_threshold_seconds": self.strike_initialization_threshold_seconds,
            "pricing_frequency_seconds": self.pricing_frequency_seconds,
            "liquidator_liquidation_percentage": self.liquidator_liquidation_percentage,
            "insurance_vault_liquidation_percentage": self.insurance_vault_liquidation_percentage,
            "native_d1_trade_fee_percentage": self.native_d1_trade_fee_percentage,
            "native_d1_underlying_fee_percentage": self.native_d1_underlying_fee_percentage,
            "native_option_trade_fee_percentage": self.native_option_trade_fee_percentage,
            "native_option_underlying_fee_percentage": self.native_option_underlying_fee_percentage,
            "native_whitelist_underlying_fee_percentage": self.native_whitelist_underlying_fee_percentage,
            "native_deposit_limit": self.native_deposit_limit,
            "expiration_threshold_seconds": self.expiration_threshold_seconds,
            "position_movement_fee_bps": self.position_movement_fee_bps,
            "margin_concession_percentage": self.margin_concession_percentage,
        }

    @classmethod
    def from_json(cls, obj: UpdateStateArgsJSON) -> "UpdateStateArgs":
        return cls(
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
            native_option_trade_fee_percentage=obj[
                "native_option_trade_fee_percentage"
            ],
            native_option_underlying_fee_percentage=obj[
                "native_option_underlying_fee_percentage"
            ],
            native_whitelist_underlying_fee_percentage=obj[
                "native_whitelist_underlying_fee_percentage"
            ],
            native_deposit_limit=obj["native_deposit_limit"],
            expiration_threshold_seconds=obj["expiration_threshold_seconds"],
            position_movement_fee_bps=obj["position_movement_fee_bps"],
            margin_concession_percentage=obj["margin_concession_percentage"],
        )
