from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class BurnVaultTokensAccounts(typing.TypedDict):
    state: PublicKey
    mint: PublicKey
    vault: PublicKey
    serum_authority: PublicKey
    token_program: PublicKey


def burn_vault_tokens(accounts: BurnVaultTokensAccounts) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["mint"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["vault"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["serum_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
    ]
    identifier = b"\xe9\xcb\xa5\xc9\xaf+\xbc\x9f"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
