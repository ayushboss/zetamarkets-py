from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class UpdateVolatilityNodesArgs(typing.TypedDict):
    nodes: list[int]


layout = borsh.CStruct("nodes" / borsh.U64[5])


class UpdateVolatilityNodesAccounts(typing.TypedDict):
    state: PublicKey
    zeta_group: PublicKey
    greeks: PublicKey
    admin: PublicKey


def update_volatility_nodes(
    args: UpdateVolatilityNodesArgs, accounts: UpdateVolatilityNodesAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["greeks"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
    ]
    identifier = b'd\xaa\xc4"H\xe4\xdb\xec'
    encoded_args = layout.build(
        {
            "nodes": args["nodes"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
