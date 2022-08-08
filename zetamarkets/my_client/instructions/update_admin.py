from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class UpdateAdminAccounts(typing.TypedDict):
    state: PublicKey
    admin: PublicKey
    new_admin: PublicKey


def update_admin(accounts: UpdateAdminAccounts) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["new_admin"], is_signer=True, is_writable=True),
    ]
    identifier = b"\xa1\xb0(\xd5<\xb8\xb3\xe4"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
