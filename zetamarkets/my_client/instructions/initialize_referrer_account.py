from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class InitializeReferrerAccountAccounts(typing.TypedDict):
    state: PublicKey
    admin: PublicKey
    referrer: PublicKey
    referrer_account: PublicKey
    system_program: PublicKey


def initialize_referrer_account(
    accounts: InitializeReferrerAccountAccounts,
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["referrer"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["referrer_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
    ]
    identifier = b"-\\\xcaDGC3\x04"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
