from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class ReferUserAccounts(typing.TypedDict):
    user: PublicKey
    referrer_account: PublicKey
    referral_account: PublicKey
    system_program: PublicKey


def refer_user(accounts: ReferUserAccounts) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["user"], is_signer=True, is_writable=True),
        AccountMeta(
            pubkey=accounts["referrer_account"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["referral_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
    ]
    identifier = b"9r\x9a\xcc\xb9!\xaa\x88"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
