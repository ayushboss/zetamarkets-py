from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class UpdatePricingHaltedArgs(typing.TypedDict):
    expiry_index: int


layout = borsh.CStruct("expiry_index" / borsh.U8)


class UpdatePricingHaltedAccounts(typing.TypedDict):
    state: PublicKey
    zeta_group: PublicKey
    greeks: PublicKey
    admin: PublicKey


def update_pricing_halted(
    args: UpdatePricingHaltedArgs, accounts: UpdatePricingHaltedAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["greeks"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
    ]
    identifier = b"\x03Gm\xf1\xa5\x0e&\x13"
    encoded_args = layout.build(
        {
            "expiry_index": args["expiry_index"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
