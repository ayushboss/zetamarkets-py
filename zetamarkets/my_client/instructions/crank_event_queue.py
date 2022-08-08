from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class CrankEventQueueAccounts(typing.TypedDict):
    state: PublicKey
    zeta_group: PublicKey
    market: PublicKey
    event_queue: PublicKey
    dex_program: PublicKey
    serum_authority: PublicKey


def crank_event_queue(accounts: CrankEventQueueAccounts) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["market"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["event_queue"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["dex_program"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["serum_authority"], is_signer=False, is_writable=False
        ),
    ]
    identifier = b"C\x85a\xdf\xb2\xbc\xeb\xb5"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
