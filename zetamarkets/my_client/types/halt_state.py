from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class HaltStateJSON(typing.TypedDict):
    halted: bool
    spot_price: int
    timestamp: int
    mark_prices_set: list[bool]
    mark_prices_set_padding: list[bool]
    market_nodes_cleaned: list[bool]
    market_nodes_cleaned_padding: list[bool]
    market_cleaned: list[bool]
    market_cleaned_padding: list[bool]


@dataclass
class HaltState:
    layout: typing.ClassVar = borsh.CStruct(
        "halted" / borsh.Bool,
        "spot_price" / borsh.U64,
        "timestamp" / borsh.U64,
        "mark_prices_set" / borsh.Bool[2],
        "mark_prices_set_padding" / borsh.Bool[4],
        "market_nodes_cleaned" / borsh.Bool[2],
        "market_nodes_cleaned_padding" / borsh.Bool[4],
        "market_cleaned" / borsh.Bool[46],
        "market_cleaned_padding" / borsh.Bool[92],
    )
    halted: bool
    spot_price: int
    timestamp: int
    mark_prices_set: list[bool]
    mark_prices_set_padding: list[bool]
    market_nodes_cleaned: list[bool]
    market_nodes_cleaned_padding: list[bool]
    market_cleaned: list[bool]
    market_cleaned_padding: list[bool]

    @classmethod
    def from_decoded(cls, obj: Container) -> "HaltState":
        return cls(
            halted=obj.halted,
            spot_price=obj.spot_price,
            timestamp=obj.timestamp,
            mark_prices_set=obj.mark_prices_set,
            mark_prices_set_padding=obj.mark_prices_set_padding,
            market_nodes_cleaned=obj.market_nodes_cleaned,
            market_nodes_cleaned_padding=obj.market_nodes_cleaned_padding,
            market_cleaned=obj.market_cleaned,
            market_cleaned_padding=obj.market_cleaned_padding,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "halted": self.halted,
            "spot_price": self.spot_price,
            "timestamp": self.timestamp,
            "mark_prices_set": self.mark_prices_set,
            "mark_prices_set_padding": self.mark_prices_set_padding,
            "market_nodes_cleaned": self.market_nodes_cleaned,
            "market_nodes_cleaned_padding": self.market_nodes_cleaned_padding,
            "market_cleaned": self.market_cleaned,
            "market_cleaned_padding": self.market_cleaned_padding,
        }

    def to_json(self) -> HaltStateJSON:
        return {
            "halted": self.halted,
            "spot_price": self.spot_price,
            "timestamp": self.timestamp,
            "mark_prices_set": self.mark_prices_set,
            "mark_prices_set_padding": self.mark_prices_set_padding,
            "market_nodes_cleaned": self.market_nodes_cleaned,
            "market_nodes_cleaned_padding": self.market_nodes_cleaned_padding,
            "market_cleaned": self.market_cleaned,
            "market_cleaned_padding": self.market_cleaned_padding,
        }

    @classmethod
    def from_json(cls, obj: HaltStateJSON) -> "HaltState":
        return cls(
            halted=obj["halted"],
            spot_price=obj["spot_price"],
            timestamp=obj["timestamp"],
            mark_prices_set=obj["mark_prices_set"],
            mark_prices_set_padding=obj["mark_prices_set_padding"],
            market_nodes_cleaned=obj["market_nodes_cleaned"],
            market_nodes_cleaned_padding=obj["market_nodes_cleaned_padding"],
            market_cleaned=obj["market_cleaned"],
            market_cleaned_padding=obj["market_cleaned_padding"],
        )
