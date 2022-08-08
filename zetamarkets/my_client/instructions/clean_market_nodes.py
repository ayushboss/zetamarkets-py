from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class CleanMarketNodesArgs(typing.TypedDict):
    expiry_index: int


layout = borsh.CStruct("expiry_index" / borsh.U8)


class CleanMarketNodesAccounts(typing.TypedDict):
    zeta_group: PublicKey
    greeks: PublicKey


def clean_market_nodes(
    args: CleanMarketNodesArgs, accounts: CleanMarketNodesAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["greeks"], is_signer=False, is_writable=True),
    ]
    identifier = b"9#\x86\xa2\x14\xd67\xe3"
    encoded_args = layout.build(
        {
            "expiry_index": args["expiry_index"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
