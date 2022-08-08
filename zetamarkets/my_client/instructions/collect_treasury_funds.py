from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class CollectTreasuryFundsArgs(typing.TypedDict):
    amount: int


layout = borsh.CStruct("amount" / borsh.U64)


class CollectTreasuryFundsAccounts(typing.TypedDict):
    state: PublicKey
    treasury_wallet: PublicKey
    collection_token_account: PublicKey
    token_program: PublicKey
    admin: PublicKey


def collect_treasury_funds(
    args: CollectTreasuryFundsArgs, accounts: CollectTreasuryFundsAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["treasury_wallet"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["collection_token_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
    ]
    identifier = b"\xf3\xd5\x04\xec\x1a\xf6\xb4\xae"
    encoded_args = layout.build(
        {
            "amount": args["amount"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
