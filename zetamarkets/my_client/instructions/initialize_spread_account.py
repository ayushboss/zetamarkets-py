from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class InitializeSpreadAccountAccounts(typing.TypedDict):
    spread_account: PublicKey
    authority: PublicKey
    payer: PublicKey
    zeta_program: PublicKey
    system_program: PublicKey
    zeta_group: PublicKey


def initialize_spread_account(
    accounts: InitializeSpreadAccountAccounts,
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["spread_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(
            pubkey=accounts["zeta_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=False),
    ]
    identifier = b"\xceV\xfb\x1b[o\x17\xd3"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
