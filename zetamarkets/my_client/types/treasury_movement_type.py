from __future__ import annotations
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh


class UndefinedJSON(typing.TypedDict):
    kind: typing.Literal["Undefined"]


class ToTreasuryJSON(typing.TypedDict):
    kind: typing.Literal["ToTreasury"]


class ToInsuranceJSON(typing.TypedDict):
    kind: typing.Literal["ToInsurance"]


@dataclass
class Undefined:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "Undefined"

    @classmethod
    def to_json(cls) -> UndefinedJSON:
        return UndefinedJSON(
            kind="Undefined",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Undefined": {},
        }


@dataclass
class ToTreasury:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "ToTreasury"

    @classmethod
    def to_json(cls) -> ToTreasuryJSON:
        return ToTreasuryJSON(
            kind="ToTreasury",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "ToTreasury": {},
        }


@dataclass
class ToInsurance:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "ToInsurance"

    @classmethod
    def to_json(cls) -> ToInsuranceJSON:
        return ToInsuranceJSON(
            kind="ToInsurance",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "ToInsurance": {},
        }


TreasuryMovementTypeKind = typing.Union[Undefined, ToTreasury, ToInsurance]
TreasuryMovementTypeJSON = typing.Union[UndefinedJSON, ToTreasuryJSON, ToInsuranceJSON]


def from_decoded(obj: dict) -> TreasuryMovementTypeKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Undefined" in obj:
        return Undefined()
    if "ToTreasury" in obj:
        return ToTreasury()
    if "ToInsurance" in obj:
        return ToInsurance()
    raise ValueError("Invalid enum object")


def from_json(obj: TreasuryMovementTypeJSON) -> TreasuryMovementTypeKind:
    if obj["kind"] == "Undefined":
        return Undefined()
    if obj["kind"] == "ToTreasury":
        return ToTreasury()
    if obj["kind"] == "ToInsurance":
        return ToInsurance()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "Undefined" / borsh.CStruct(),
    "ToTreasury" / borsh.CStruct(),
    "ToInsurance" / borsh.CStruct(),
)
