from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class HaltZetaGroupArgsJSON(typing.TypedDict):
    spot_price: int
    timestamp: int


@dataclass
class HaltZetaGroupArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "spot_price" / borsh.U64, "timestamp" / borsh.U64
    )
    spot_price: int
    timestamp: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "HaltZetaGroupArgs":
        return cls(spot_price=obj.spot_price, timestamp=obj.timestamp)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"spot_price": self.spot_price, "timestamp": self.timestamp}

    def to_json(self) -> HaltZetaGroupArgsJSON:
        return {"spot_price": self.spot_price, "timestamp": self.timestamp}

    @classmethod
    def from_json(cls, obj: HaltZetaGroupArgsJSON) -> "HaltZetaGroupArgs":
        return cls(spot_price=obj["spot_price"], timestamp=obj["timestamp"])
