from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class SettleDexFundsAccounts(typing.TypedDict):
    state: PublicKey
    market: PublicKey
    zeta_base_vault: PublicKey
    zeta_quote_vault: PublicKey
    dex_base_vault: PublicKey
    dex_quote_vault: PublicKey
    vault_owner: PublicKey
    mint_authority: PublicKey
    serum_authority: PublicKey
    dex_program: PublicKey
    token_program: PublicKey


def settle_dex_funds(accounts: SettleDexFundsAccounts) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["market"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["zeta_base_vault"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["zeta_quote_vault"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["dex_base_vault"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["dex_quote_vault"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["vault_owner"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["mint_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["serum_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["dex_program"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
    ]
    identifier = b"\xa5g\x8e&\xd3\xa6\x0e\xe2"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
