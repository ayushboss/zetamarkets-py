from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class MarginParametersJSON(typing.TypedDict):
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
    padding: list[int]


@dataclass
class MarginParameters:
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
        "padding" / borsh.U8[32],
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
    padding: list[int]

    @classmethod
    def from_decoded(cls, obj: Container) -> "MarginParameters":
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
            padding=obj.padding,
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
            "padding": self.padding,
        }

    def to_json(self) -> MarginParametersJSON:
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
            "padding": self.padding,
        }

    @classmethod
    def from_json(cls, obj: MarginParametersJSON) -> "MarginParameters":
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
            padding=obj["padding"],
        )
