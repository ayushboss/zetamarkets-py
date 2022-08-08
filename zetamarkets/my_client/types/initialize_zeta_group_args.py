from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class InitializeZetaGroupArgsJSON(typing.TypedDict):
    zeta_group_nonce: int
    underlying_nonce: int
    greeks_nonce: int
    vault_nonce: int
    insurance_vault_nonce: int
    socialized_loss_account_nonce: int
    interest_rate: int
    volatility: list[int]
    option_trade_normalizer: int
    future_trade_normalizer: int
    max_volatility_retreat: int
    max_interest_retreat: int
    max_delta: int
    min_delta: int
    min_interest_rate: int
    max_interest_rate: int
    min_volatility: int
    max_volatility: int
    future_margin_initial: int
    future_margin_maintenance: int
    option_mark_percentage_long_initial: int
    option_spot_percentage_long_initial: int
    option_spot_percentage_short_initial: int
    option_dynamic_percentage_short_initial: int
    option_mark_percentage_long_maintenance: int
    option_spot_percentage_long_maintenance: int
    option_spot_percentage_short_maintenance: int
    option_dynamic_percentage_short_maintenance: int
    option_short_put_cap_percentage: int


@dataclass
class InitializeZetaGroupArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "zeta_group_nonce" / borsh.U8,
        "underlying_nonce" / borsh.U8,
        "greeks_nonce" / borsh.U8,
        "vault_nonce" / borsh.U8,
        "insurance_vault_nonce" / borsh.U8,
        "socialized_loss_account_nonce" / borsh.U8,
        "interest_rate" / borsh.I64,
        "volatility" / borsh.U64[5],
        "option_trade_normalizer" / borsh.U64,
        "future_trade_normalizer" / borsh.U64,
        "max_volatility_retreat" / borsh.U64,
        "max_interest_retreat" / borsh.U64,
        "max_delta" / borsh.U64,
        "min_delta" / borsh.U64,
        "min_interest_rate" / borsh.I64,
        "max_interest_rate" / borsh.I64,
        "min_volatility" / borsh.U64,
        "max_volatility" / borsh.U64,
        "future_margin_initial" / borsh.U64,
        "future_margin_maintenance" / borsh.U64,
        "option_mark_percentage_long_initial" / borsh.U64,
        "option_spot_percentage_long_initial" / borsh.U64,
        "option_spot_percentage_short_initial" / borsh.U64,
        "option_dynamic_percentage_short_initial" / borsh.U64,
        "option_mark_percentage_long_maintenance" / borsh.U64,
        "option_spot_percentage_long_maintenance" / borsh.U64,
        "option_spot_percentage_short_maintenance" / borsh.U64,
        "option_dynamic_percentage_short_maintenance" / borsh.U64,
        "option_short_put_cap_percentage" / borsh.U64,
    )
    zeta_group_nonce: int
    underlying_nonce: int
    greeks_nonce: int
    vault_nonce: int
    insurance_vault_nonce: int
    socialized_loss_account_nonce: int
    interest_rate: int
    volatility: list[int]
    option_trade_normalizer: int
    future_trade_normalizer: int
    max_volatility_retreat: int
    max_interest_retreat: int
    max_delta: int
    min_delta: int
    min_interest_rate: int
    max_interest_rate: int
    min_volatility: int
    max_volatility: int
    future_margin_initial: int
    future_margin_maintenance: int
    option_mark_percentage_long_initial: int
    option_spot_percentage_long_initial: int
    option_spot_percentage_short_initial: int
    option_dynamic_percentage_short_initial: int
    option_mark_percentage_long_maintenance: int
    option_spot_percentage_long_maintenance: int
    option_spot_percentage_short_maintenance: int
    option_dynamic_percentage_short_maintenance: int
    option_short_put_cap_percentage: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "InitializeZetaGroupArgs":
        return cls(
            zeta_group_nonce=obj.zeta_group_nonce,
            underlying_nonce=obj.underlying_nonce,
            greeks_nonce=obj.greeks_nonce,
            vault_nonce=obj.vault_nonce,
            insurance_vault_nonce=obj.insurance_vault_nonce,
            socialized_loss_account_nonce=obj.socialized_loss_account_nonce,
            interest_rate=obj.interest_rate,
            volatility=obj.volatility,
            option_trade_normalizer=obj.option_trade_normalizer,
            future_trade_normalizer=obj.future_trade_normalizer,
            max_volatility_retreat=obj.max_volatility_retreat,
            max_interest_retreat=obj.max_interest_retreat,
            max_delta=obj.max_delta,
            min_delta=obj.min_delta,
            min_interest_rate=obj.min_interest_rate,
            max_interest_rate=obj.max_interest_rate,
            min_volatility=obj.min_volatility,
            max_volatility=obj.max_volatility,
            future_margin_initial=obj.future_margin_initial,
            future_margin_maintenance=obj.future_margin_maintenance,
            option_mark_percentage_long_initial=obj.option_mark_percentage_long_initial,
            option_spot_percentage_long_initial=obj.option_spot_percentage_long_initial,
            option_spot_percentage_short_initial=obj.option_spot_percentage_short_initial,
            option_dynamic_percentage_short_initial=obj.option_dynamic_percentage_short_initial,
            option_mark_percentage_long_maintenance=obj.option_mark_percentage_long_maintenance,
            option_spot_percentage_long_maintenance=obj.option_spot_percentage_long_maintenance,
            option_spot_percentage_short_maintenance=obj.option_spot_percentage_short_maintenance,
            option_dynamic_percentage_short_maintenance=obj.option_dynamic_percentage_short_maintenance,
            option_short_put_cap_percentage=obj.option_short_put_cap_percentage,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "zeta_group_nonce": self.zeta_group_nonce,
            "underlying_nonce": self.underlying_nonce,
            "greeks_nonce": self.greeks_nonce,
            "vault_nonce": self.vault_nonce,
            "insurance_vault_nonce": self.insurance_vault_nonce,
            "socialized_loss_account_nonce": self.socialized_loss_account_nonce,
            "interest_rate": self.interest_rate,
            "volatility": self.volatility,
            "option_trade_normalizer": self.option_trade_normalizer,
            "future_trade_normalizer": self.future_trade_normalizer,
            "max_volatility_retreat": self.max_volatility_retreat,
            "max_interest_retreat": self.max_interest_retreat,
            "max_delta": self.max_delta,
            "min_delta": self.min_delta,
            "min_interest_rate": self.min_interest_rate,
            "max_interest_rate": self.max_interest_rate,
            "min_volatility": self.min_volatility,
            "max_volatility": self.max_volatility,
            "future_margin_initial": self.future_margin_initial,
            "future_margin_maintenance": self.future_margin_maintenance,
            "option_mark_percentage_long_initial": self.option_mark_percentage_long_initial,
            "option_spot_percentage_long_initial": self.option_spot_percentage_long_initial,
            "option_spot_percentage_short_initial": self.option_spot_percentage_short_initial,
            "option_dynamic_percentage_short_initial": self.option_dynamic_percentage_short_initial,
            "option_mark_percentage_long_maintenance": self.option_mark_percentage_long_maintenance,
            "option_spot_percentage_long_maintenance": self.option_spot_percentage_long_maintenance,
            "option_spot_percentage_short_maintenance": self.option_spot_percentage_short_maintenance,
            "option_dynamic_percentage_short_maintenance": self.option_dynamic_percentage_short_maintenance,
            "option_short_put_cap_percentage": self.option_short_put_cap_percentage,
        }

    def to_json(self) -> InitializeZetaGroupArgsJSON:
        return {
            "zeta_group_nonce": self.zeta_group_nonce,
            "underlying_nonce": self.underlying_nonce,
            "greeks_nonce": self.greeks_nonce,
            "vault_nonce": self.vault_nonce,
            "insurance_vault_nonce": self.insurance_vault_nonce,
            "socialized_loss_account_nonce": self.socialized_loss_account_nonce,
            "interest_rate": self.interest_rate,
            "volatility": self.volatility,
            "option_trade_normalizer": self.option_trade_normalizer,
            "future_trade_normalizer": self.future_trade_normalizer,
            "max_volatility_retreat": self.max_volatility_retreat,
            "max_interest_retreat": self.max_interest_retreat,
            "max_delta": self.max_delta,
            "min_delta": self.min_delta,
            "min_interest_rate": self.min_interest_rate,
            "max_interest_rate": self.max_interest_rate,
            "min_volatility": self.min_volatility,
            "max_volatility": self.max_volatility,
            "future_margin_initial": self.future_margin_initial,
            "future_margin_maintenance": self.future_margin_maintenance,
            "option_mark_percentage_long_initial": self.option_mark_percentage_long_initial,
            "option_spot_percentage_long_initial": self.option_spot_percentage_long_initial,
            "option_spot_percentage_short_initial": self.option_spot_percentage_short_initial,
            "option_dynamic_percentage_short_initial": self.option_dynamic_percentage_short_initial,
            "option_mark_percentage_long_maintenance": self.option_mark_percentage_long_maintenance,
            "option_spot_percentage_long_maintenance": self.option_spot_percentage_long_maintenance,
            "option_spot_percentage_short_maintenance": self.option_spot_percentage_short_maintenance,
            "option_dynamic_percentage_short_maintenance": self.option_dynamic_percentage_short_maintenance,
            "option_short_put_cap_percentage": self.option_short_put_cap_percentage,
        }

    @classmethod
    def from_json(cls, obj: InitializeZetaGroupArgsJSON) -> "InitializeZetaGroupArgs":
        return cls(
            zeta_group_nonce=obj["zeta_group_nonce"],
            underlying_nonce=obj["underlying_nonce"],
            greeks_nonce=obj["greeks_nonce"],
            vault_nonce=obj["vault_nonce"],
            insurance_vault_nonce=obj["insurance_vault_nonce"],
            socialized_loss_account_nonce=obj["socialized_loss_account_nonce"],
            interest_rate=obj["interest_rate"],
            volatility=obj["volatility"],
            option_trade_normalizer=obj["option_trade_normalizer"],
            future_trade_normalizer=obj["future_trade_normalizer"],
            max_volatility_retreat=obj["max_volatility_retreat"],
            max_interest_retreat=obj["max_interest_retreat"],
            max_delta=obj["max_delta"],
            min_delta=obj["min_delta"],
            min_interest_rate=obj["min_interest_rate"],
            max_interest_rate=obj["max_interest_rate"],
            min_volatility=obj["min_volatility"],
            max_volatility=obj["max_volatility"],
            future_margin_initial=obj["future_margin_initial"],
            future_margin_maintenance=obj["future_margin_maintenance"],
            option_mark_percentage_long_initial=obj[
                "option_mark_percentage_long_initial"
            ],
            option_spot_percentage_long_initial=obj[
                "option_spot_percentage_long_initial"
            ],
            option_spot_percentage_short_initial=obj[
                "option_spot_percentage_short_initial"
            ],
            option_dynamic_percentage_short_initial=obj[
                "option_dynamic_percentage_short_initial"
            ],
            option_mark_percentage_long_maintenance=obj[
                "option_mark_percentage_long_maintenance"
            ],
            option_spot_percentage_long_maintenance=obj[
                "option_spot_percentage_long_maintenance"
            ],
            option_spot_percentage_short_maintenance=obj[
                "option_spot_percentage_short_maintenance"
            ],
            option_dynamic_percentage_short_maintenance=obj[
                "option_dynamic_percentage_short_maintenance"
            ],
            option_short_put_cap_percentage=obj["option_short_put_cap_percentage"],
        )
