from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class ForceCancelOrdersAccounts(typing.TypedDict):
    greeks: PublicKey
    oracle: PublicKey
    cancel_accounts: CancelAccountsNested


class CancelAccountsNested(typing.TypedDict):
    zeta_group: PublicKey
    state: PublicKey
    margin_account: PublicKey
    dex_program: PublicKey
    serum_authority: PublicKey
    open_orders: PublicKey
    market: PublicKey
    bids: PublicKey
    asks: PublicKey
    event_queue: PublicKey


def force_cancel_orders(accounts: ForceCancelOrdersAccounts) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["greeks"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["oracle"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["zeta_group"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["state"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["margin_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["dex_program"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["serum_authority"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["open_orders"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["market"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["bids"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["asks"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["event_queue"],
            is_signer=False,
            is_writable=True,
        ),
    ]
    identifier = b"@\xb5\xc4?\xdeH@\xe8"
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
