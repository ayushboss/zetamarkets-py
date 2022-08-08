from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class AddMarketIndexesAccounts(typing.TypedDict):
    market_indexes: PublicKey
    zeta_group: PublicKey


def add_market_indexes(accounts: AddMarketIndexesAccounts) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["market_indexes"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=True),
    ]
    identifier = b"^\xf6\x90\xaf\x04\xa4\xe9\xfc"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
