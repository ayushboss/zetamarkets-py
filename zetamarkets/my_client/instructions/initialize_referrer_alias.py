from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class InitializeReferrerAliasArgs(typing.TypedDict):
    alias: str


layout = borsh.CStruct("alias" / borsh.String)


class InitializeReferrerAliasAccounts(typing.TypedDict):
    referrer: PublicKey
    referrer_alias: PublicKey
    referrer_account: PublicKey
    system_program: PublicKey


def initialize_referrer_alias(
    args: InitializeReferrerAliasArgs, accounts: InitializeReferrerAliasAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["referrer"], is_signer=True, is_writable=True),
        AccountMeta(
            pubkey=accounts["referrer_alias"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["referrer_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
    ]
    identifier = b"C\x1c\x03N\x8cl\x14\x8a"
    encoded_args = layout.build(
        {
            "alias": args["alias"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
