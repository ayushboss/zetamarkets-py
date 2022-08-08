from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class ToggleMarketMakerArgs(typing.TypedDict):
    is_market_maker: bool


layout = borsh.CStruct("is_market_maker" / borsh.Bool)


class ToggleMarketMakerAccounts(typing.TypedDict):
    state: PublicKey
    admin: PublicKey
    margin_account: PublicKey


def toggle_market_maker(
    args: ToggleMarketMakerArgs, accounts: ToggleMarketMakerAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
        AccountMeta(
            pubkey=accounts["margin_account"], is_signer=False, is_writable=True
        ),
    ]
    identifier = b"\xcb\xf7T\x9fh\xfd\x94P"
    encoded_args = layout.build(
        {
            "is_market_maker": args["is_market_maker"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
