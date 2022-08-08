from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class InitializeWhitelistInsuranceAccountArgs(typing.TypedDict):
    nonce: int


layout = borsh.CStruct("nonce" / borsh.U8)


class InitializeWhitelistInsuranceAccountAccounts(typing.TypedDict):
    whitelist_insurance_account: PublicKey
    admin: PublicKey
    user: PublicKey
    system_program: PublicKey
    state: PublicKey


def initialize_whitelist_insurance_account(
    args: InitializeWhitelistInsuranceAccountArgs,
    accounts: InitializeWhitelistInsuranceAccountAccounts,
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["whitelist_insurance_account"],
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
    identifier = b"+.\xf0\x9bP\x04Vf"
    encoded_args = layout.build(
        {
            "nonce": args["nonce"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
