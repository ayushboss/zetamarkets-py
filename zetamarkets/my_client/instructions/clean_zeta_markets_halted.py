from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class CleanZetaMarketsHaltedAccounts(typing.TypedDict):
    state: PublicKey
    zeta_group: PublicKey


def clean_zeta_markets_halted(
    accounts: CleanZetaMarketsHaltedAccounts,
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=True),
    ]
    identifier = b"\x7f\xe4\x10\xf4SD\x96^"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
