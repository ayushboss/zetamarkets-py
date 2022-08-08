from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class OverrideExpiryArgs(typing.TypedDict):
    args: types.override_expiry_args.OverrideExpiryArgs


layout = borsh.CStruct("args" / types.override_expiry_args.OverrideExpiryArgs.layout)


class OverrideExpiryAccounts(typing.TypedDict):
    state: PublicKey
    admin: PublicKey
    zeta_group: PublicKey


def override_expiry(
    args: OverrideExpiryArgs, accounts: OverrideExpiryAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=True),
    ]
    identifier = b"\x81\xc5urlw\xcf\x88"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
