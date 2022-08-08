from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class WithdrawArgs(typing.TypedDict):
    amount: int


layout = borsh.CStruct("amount" / borsh.U64)


class WithdrawAccounts(typing.TypedDict):
    state: PublicKey
    zeta_group: PublicKey
    vault: PublicKey
    margin_account: PublicKey
    user_token_account: PublicKey
    token_program: PublicKey
    authority: PublicKey
    greeks: PublicKey
    oracle: PublicKey
    socialized_loss_account: PublicKey


def withdraw(args: WithdrawArgs, accounts: WithdrawAccounts) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["vault"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["margin_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["user_token_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["greeks"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["oracle"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["socialized_loss_account"],
            is_signer=False,
            is_writable=True,
        ),
    ]
    identifier = b'\xb7\x12F\x9c\x94m\xa1"'
    encoded_args = layout.build(
        {
            "amount": args["amount"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
