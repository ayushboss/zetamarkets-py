from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class ExpireSeriesArgs(typing.TypedDict):
    settlement_nonce: int


layout = borsh.CStruct("settlement_nonce" / borsh.U8)


class ExpireSeriesAccounts(typing.TypedDict):
    state: PublicKey
    zeta_group: PublicKey
    oracle: PublicKey
    settlement_account: PublicKey
    payer: PublicKey
    system_program: PublicKey
    greeks: PublicKey


def expire_series(
    args: ExpireSeriesArgs, accounts: ExpireSeriesAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["oracle"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["settlement_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["greeks"], is_signer=False, is_writable=True),
    ]
    identifier = b"-\xa2ib,\x15\xab\x7f"
    encoded_args = layout.build(
        {
            "settlement_nonce": args["settlement_nonce"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
