from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class InitializeMarketNodeArgs(typing.TypedDict):
    args: types.initialize_market_node_args.InitializeMarketNodeArgs


layout = borsh.CStruct(
    "args" / types.initialize_market_node_args.InitializeMarketNodeArgs.layout
)


class InitializeMarketNodeAccounts(typing.TypedDict):
    zeta_group: PublicKey
    market_node: PublicKey
    greeks: PublicKey
    payer: PublicKey
    system_program: PublicKey


def initialize_market_node(
    args: InitializeMarketNodeArgs, accounts: InitializeMarketNodeAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["market_node"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["greeks"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
    ]
    identifier = b"2v\x15\x15\xb3\xf8\x17\x80"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
