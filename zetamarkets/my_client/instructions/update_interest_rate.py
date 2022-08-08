from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class UpdateInterestRateArgs(typing.TypedDict):
    args: types.update_interest_rate_args.UpdateInterestRateArgs


layout = borsh.CStruct(
    "args" / types.update_interest_rate_args.UpdateInterestRateArgs.layout
)


class UpdateInterestRateAccounts(typing.TypedDict):
    state: PublicKey
    greeks: PublicKey
    zeta_group: PublicKey
    admin: PublicKey


def update_interest_rate(
    args: UpdateInterestRateArgs, accounts: UpdateInterestRateAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["greeks"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
    ]
    identifier = b"K\x08\xff){;\x87\xee"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
