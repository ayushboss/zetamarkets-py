from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class UpdateMarginParametersArgsJSON(typing.TypedDict):
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
class UpdateMarginParametersArgs:
    layout: typing.ClassVar = borsh.CStruct(
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
    def from_decoded(cls, obj: Container) -> "UpdateMarginParametersArgs":
        return cls(
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

    def to_json(self) -> UpdateMarginParametersArgsJSON:
        return {
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
    def from_json(
        cls, obj: UpdateMarginParametersArgsJSON
    ) -> "UpdateMarginParametersArgs":
        return cls(
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
