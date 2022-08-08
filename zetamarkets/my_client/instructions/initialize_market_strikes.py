from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class InitializeMarketStrikesAccounts(typing.TypedDict):
    state: PublicKey
    zeta_group: PublicKey
    oracle: PublicKey


def initialize_market_strikes(
    accounts: InitializeMarketStrikesAccounts,
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["oracle"], is_signer=False, is_writable=False),
    ]
    identifier = b"\xbd.\xff!~\x85+\xab"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
