from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class RebalanceInsuranceVaultAccounts(typing.TypedDict):
    state: PublicKey
    zeta_group: PublicKey
    zeta_vault: PublicKey
    insurance_vault: PublicKey
    treasury_wallet: PublicKey
    socialized_loss_account: PublicKey
    token_program: PublicKey


def rebalance_insurance_vault(
    accounts: RebalanceInsuranceVaultAccounts,
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_vault"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["insurance_vault"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["treasury_wallet"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["socialized_loss_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
    ]
    identifier = b"\x0b\xc4B\xeb;\xed\xdfo"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
