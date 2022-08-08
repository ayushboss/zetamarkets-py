from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class InitializeOpenOrdersAccounts(typing.TypedDict):
    state: PublicKey
    zeta_group: PublicKey
    dex_program: PublicKey
    system_program: PublicKey
    open_orders: PublicKey
    margin_account: PublicKey
    authority: PublicKey
    payer: PublicKey
    market: PublicKey
    serum_authority: PublicKey
    open_orders_map: PublicKey
    rent: PublicKey


def initialize_open_orders(
    accounts: InitializeOpenOrdersAccounts,
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["dex_program"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["open_orders"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["margin_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["market"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["serum_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["open_orders_map"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["rent"], is_signer=False, is_writable=False),
    ]
    identifier = b"7\xea\x10Rd*~\xc0"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
