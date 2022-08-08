from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class HaltZetaGroupAccounts(typing.TypedDict):
    state: PublicKey
    zeta_group: PublicKey
    greeks: PublicKey
    admin: PublicKey


def halt_zeta_group(accounts: HaltZetaGroupAccounts) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["greeks"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
    ]
    identifier = b"\x1bCr\xf4\xc4}\x92u"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
