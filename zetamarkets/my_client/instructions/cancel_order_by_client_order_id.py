from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class CancelOrderByClientOrderIdArgs(typing.TypedDict):
    client_order_id: int


layout = borsh.CStruct("client_order_id" / borsh.U64)


class CancelOrderByClientOrderIdAccounts(typing.TypedDict):
    authority: PublicKey
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


def cancel_order_by_client_order_id(
    args: CancelOrderByClientOrderIdArgs, accounts: CancelOrderByClientOrderIdAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
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
    identifier = b"s\xb2\xc9\x08\xaf\xb7{w"
    encoded_args = layout.build(
        {
            "client_order_id": args["client_order_id"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
