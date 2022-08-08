from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class UpdatePricingArgs(typing.TypedDict):
    expiry_index: int


layout = borsh.CStruct("expiry_index" / borsh.U8)


class UpdatePricingAccounts(typing.TypedDict):
    state: PublicKey
    zeta_group: PublicKey
    greeks: PublicKey
    oracle: PublicKey


def update_pricing(
    args: UpdatePricingArgs, accounts: UpdatePricingAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["greeks"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["oracle"], is_signer=False, is_writable=False),
    ]
    identifier = b"\x9d\xe1\xd0\x96\x17\x99\xfd\x12"
    encoded_args = layout.build(
        {
            "expiry_index": args["expiry_index"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
