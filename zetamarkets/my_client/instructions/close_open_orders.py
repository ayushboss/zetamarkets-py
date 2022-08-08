from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class CloseOpenOrdersArgs(typing.TypedDict):
    map_nonce: int


layout = borsh.CStruct("map_nonce" / borsh.U8)


class CloseOpenOrdersAccounts(typing.TypedDict):
    state: PublicKey
    zeta_group: PublicKey
    dex_program: PublicKey
    open_orders: PublicKey
    margin_account: PublicKey
    authority: PublicKey
    market: PublicKey
    serum_authority: PublicKey
    open_orders_map: PublicKey


def close_open_orders(
    args: CloseOpenOrdersArgs, accounts: CloseOpenOrdersAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["dex_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["open_orders"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["margin_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["market"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["serum_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["open_orders_map"], is_signer=False, is_writable=True
        ),
    ]
    identifier = b"\xc8\xd8?\xef\x07\xe6\xff\x14"
    encoded_args = layout.build(
        {
            "map_nonce": args["map_nonce"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
