from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class UpdateHaltStateArgs(typing.TypedDict):
    args: types.halt_zeta_group_args.HaltZetaGroupArgs


layout = borsh.CStruct("args" / types.halt_zeta_group_args.HaltZetaGroupArgs.layout)


class UpdateHaltStateAccounts(typing.TypedDict):
    state: PublicKey
    zeta_group: PublicKey
    admin: PublicKey


def update_halt_state(
    args: UpdateHaltStateArgs, accounts: UpdateHaltStateAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
    ]
    identifier = b"\xd7-5\xa2\x95\x8a\x05?"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
