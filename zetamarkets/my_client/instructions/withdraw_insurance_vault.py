from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class WithdrawInsuranceVaultArgs(typing.TypedDict):
    percentage_amount: int


layout = borsh.CStruct("percentage_amount" / borsh.U64)


class WithdrawInsuranceVaultAccounts(typing.TypedDict):
    zeta_group: PublicKey
    insurance_vault: PublicKey
    insurance_deposit_account: PublicKey
    user_token_account: PublicKey
    authority: PublicKey
    token_program: PublicKey


def withdraw_insurance_vault(
    args: WithdrawInsuranceVaultArgs, accounts: WithdrawInsuranceVaultAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["insurance_vault"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["insurance_deposit_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["user_token_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
    ]
    identifier = b"\x11\xfa\xd5-\xacuQ\xe1"
    encoded_args = layout.build(
        {
            "percentage_amount": args["percentage_amount"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
