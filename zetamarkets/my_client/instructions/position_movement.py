from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from construct import Construct
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class PositionMovementArgs(typing.TypedDict):
    movement_type: types.movement_type.MovementTypeKind
    movements: list[types.position_movement_arg.PositionMovementArg]


layout = borsh.CStruct(
    "movement_type" / types.movement_type.layout,
    "movements"
    / borsh.Vec(
        typing.cast(Construct, types.position_movement_arg.PositionMovementArg.layout)
    ),
)


class PositionMovementAccounts(typing.TypedDict):
    state: PublicKey
    zeta_group: PublicKey
    margin_account: PublicKey
    spread_account: PublicKey
    authority: PublicKey
    greeks: PublicKey
    oracle: PublicKey


def position_movement(
    args: PositionMovementArgs, accounts: PositionMovementAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["margin_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["spread_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["greeks"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["oracle"], is_signer=False, is_writable=False),
    ]
    identifier = b"u\x10K\xf9\xb3\x7f\xab\x93"
    encoded_args = layout.build(
        {
            "movement_type": args["movement_type"].to_encodable(),
            "movements": list(map(lambda item: item.to_encodable(), args["movements"])),
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
