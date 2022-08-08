from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class InitializeInsuranceDepositAccountArgs(typing.TypedDict):
    nonce: int


layout = borsh.CStruct("nonce" / borsh.U8)


class InitializeInsuranceDepositAccountAccounts(typing.TypedDict):
    zeta_group: PublicKey
    insurance_deposit_account: PublicKey
    authority: PublicKey
    system_program: PublicKey
    whitelist_insurance_account: PublicKey


def initialize_insurance_deposit_account(
    args: InitializeInsuranceDepositAccountArgs,
    accounts: InitializeInsuranceDepositAccountAccounts,
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["insurance_deposit_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=True),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["whitelist_insurance_account"],
            is_signer=False,
            is_writable=False,
        ),
    ]
    identifier = b"U\xa3ry\x8b\xa7)%"
    encoded_args = layout.build(
        {
            "nonce": args["nonce"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
