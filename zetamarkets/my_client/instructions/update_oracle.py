from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class UpdateOracleAccounts(typing.TypedDict):
    state: PublicKey
    zeta_group: PublicKey
    admin: PublicKey
    oracle: PublicKey


def update_oracle(accounts: UpdateOracleAccounts) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["oracle"], is_signer=False, is_writable=False),
    ]
    identifier = b"p)\xd1\x12\xf8\xe2\xfc\xbc"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
