from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class TransferExcessSpreadBalanceAccounts(typing.TypedDict):
    zeta_group: PublicKey
    margin_account: PublicKey
    spread_account: PublicKey
    authority: PublicKey


def transfer_excess_spread_balance(
    accounts: TransferExcessSpreadBalanceAccounts,
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["margin_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["spread_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
    ]
    identifier = b"\xac\xb8\x0c\n4i@\xd5"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
