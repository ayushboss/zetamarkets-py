from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class InitializeZetaTreasuryWalletAccounts(typing.TypedDict):
    state: PublicKey
    treasury_wallet: PublicKey
    rent: PublicKey
    system_program: PublicKey
    token_program: PublicKey
    usdc_mint: PublicKey
    admin: PublicKey


def initialize_zeta_treasury_wallet(
    accounts: InitializeZetaTreasuryWalletAccounts,
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["treasury_wallet"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["rent"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["usdc_mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=True),
    ]
    identifier = b"\xf99\xbbf\xb8h%\xe7"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
