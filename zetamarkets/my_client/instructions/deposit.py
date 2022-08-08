from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class DepositArgs(typing.TypedDict):
    amount: int


layout = borsh.CStruct("amount" / borsh.U64)


class DepositAccounts(typing.TypedDict):
    zeta_group: PublicKey
    margin_account: PublicKey
    vault: PublicKey
    user_token_account: PublicKey
    socialized_loss_account: PublicKey
    authority: PublicKey
    token_program: PublicKey
    state: PublicKey
    greeks: PublicKey


def deposit(args: DepositArgs, accounts: DepositAccounts) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["margin_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["vault"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["user_token_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["socialized_loss_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["greeks"], is_signer=False, is_writable=False),
    ]
    identifier = b"\xf2#\xc6\x89R\xe1\xf2\xb6"
    encoded_args = layout.build(
        {
            "amount": args["amount"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
