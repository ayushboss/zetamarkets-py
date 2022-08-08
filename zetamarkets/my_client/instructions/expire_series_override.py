from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class ExpireSeriesOverrideArgs(typing.TypedDict):
    args: types.expire_series_override_args.ExpireSeriesOverrideArgs


layout = borsh.CStruct(
    "args" / types.expire_series_override_args.ExpireSeriesOverrideArgs.layout
)


class ExpireSeriesOverrideAccounts(typing.TypedDict):
    state: PublicKey
    zeta_group: PublicKey
    settlement_account: PublicKey
    admin: PublicKey
    system_program: PublicKey
    greeks: PublicKey


def expire_series_override(
    args: ExpireSeriesOverrideArgs, accounts: ExpireSeriesOverrideAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["settlement_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=True),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["greeks"], is_signer=False, is_writable=True),
    ]
    identifier = b'h\x16"{V\xe0\x82F'
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
