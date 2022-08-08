from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class InitializeWhitelistDepositAccountArgs(typing.TypedDict):
    nonce: int


layout = borsh.CStruct("nonce" / borsh.U8)


class InitializeWhitelistDepositAccountAccounts(typing.TypedDict):
    whitelist_deposit_account: PublicKey
    admin: PublicKey
    user: PublicKey
    system_program: PublicKey
    state: PublicKey


def initialize_whitelist_deposit_account(
    args: InitializeWhitelistDepositAccountArgs,
    accounts: InitializeWhitelistDepositAccountAccounts,
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["whitelist_deposit_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["user"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
    ]
    identifier = b"=\xe7s\xdbQ\xf3\x9e\x8a"
    encoded_args = layout.build(
        {
            "nonce": args["nonce"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
