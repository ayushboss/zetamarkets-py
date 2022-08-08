from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class InitializeMarketIndexesArgs(typing.TypedDict):
    nonce: int


layout = borsh.CStruct("nonce" / borsh.U8)


class InitializeMarketIndexesAccounts(typing.TypedDict):
    state: PublicKey
    market_indexes: PublicKey
    admin: PublicKey
    system_program: PublicKey
    zeta_group: PublicKey


def initialize_market_indexes(
    args: InitializeMarketIndexesArgs, accounts: InitializeMarketIndexesAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["market_indexes"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=True),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=False),
    ]
    identifier = b"[?\xcd\x90\x14S\xb1x"
    encoded_args = layout.build(
        {
            "nonce": args["nonce"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
