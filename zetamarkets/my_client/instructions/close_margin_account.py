from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class CloseMarginAccountAccounts(typing.TypedDict):
    margin_account: PublicKey
    authority: PublicKey
    zeta_group: PublicKey


def close_margin_account(
    accounts: CloseMarginAccountAccounts,
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["margin_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=False),
    ]
    identifier = b"i\xd7)\xef\xa6\xcf\x01g"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
