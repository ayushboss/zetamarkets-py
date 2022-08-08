from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class UpdateZetaStateArgs(typing.TypedDict):
    args: types.update_state_args.UpdateStateArgs


layout = borsh.CStruct("args" / types.update_state_args.UpdateStateArgs.layout)


class UpdateZetaStateAccounts(typing.TypedDict):
    state: PublicKey
    admin: PublicKey


def update_zeta_state(
    args: UpdateZetaStateArgs, accounts: UpdateZetaStateAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
    ]
    identifier = b"h\xb6\x14\xbb\x03\xa4<\x03"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
