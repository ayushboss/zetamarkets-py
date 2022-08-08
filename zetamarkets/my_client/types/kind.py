from __future__ import annotations
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh


class UninitializedJSON(typing.TypedDict):
    kind: typing.Literal["Uninitialized"]


class CallJSON(typing.TypedDict):
    kind: typing.Literal["Call"]


class PutJSON(typing.TypedDict):
    kind: typing.Literal["Put"]


class FutureJSON(typing.TypedDict):
    kind: typing.Literal["Future"]


@dataclass
class Uninitialized:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "Uninitialized"

    @classmethod
    def to_json(cls) -> UninitializedJSON:
        return UninitializedJSON(
            kind="Uninitialized",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Uninitialized": {},
        }


@dataclass
class Call:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "Call"

    @classmethod
    def to_json(cls) -> CallJSON:
        return CallJSON(
            kind="Call",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Call": {},
        }


@dataclass
class Put:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "Put"

    @classmethod
    def to_json(cls) -> PutJSON:
        return PutJSON(
            kind="Put",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Put": {},
        }


@dataclass
class Future:
    discriminator: typing.ClassVar = 3
    kind: typing.ClassVar = "Future"

    @classmethod
    def to_json(cls) -> FutureJSON:
        return FutureJSON(
            kind="Future",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Future": {},
        }


KindKind = typing.Union[Uninitialized, Call, Put, Future]
KindJSON = typing.Union[UninitializedJSON, CallJSON, PutJSON, FutureJSON]


def from_decoded(obj: dict) -> KindKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Uninitialized" in obj:
        return Uninitialized()
    if "Call" in obj:
        return Call()
    if "Put" in obj:
        return Put()
    if "Future" in obj:
        return Future()
    raise ValueError("Invalid enum object")


def from_json(obj: KindJSON) -> KindKind:
    if obj["kind"] == "Uninitialized":
        return Uninitialized()
    if obj["kind"] == "Call":
        return Call()
    if obj["kind"] == "Put":
        return Put()
    if obj["kind"] == "Future":
        return Future()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "Uninitialized" / borsh.CStruct(),
    "Call" / borsh.CStruct(),
    "Put" / borsh.CStruct(),
    "Future" / borsh.CStruct(),
)
