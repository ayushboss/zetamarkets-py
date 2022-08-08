from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class CloseSpreadAccountAccounts(typing.TypedDict):
    spread_account: PublicKey
    authority: PublicKey
    zeta_group: PublicKey


def close_spread_account(
    accounts: CloseSpreadAccountAccounts,
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["spread_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=False),
    ]
    identifier = b"\xbe\xe4\xfd\x10\xc9\x94\xa1\xf0"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
