from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class LiquidateArgs(typing.TypedDict):
    size: int


layout = borsh.CStruct("size" / borsh.U64)


class LiquidateAccounts(typing.TypedDict):
    state: PublicKey
    liquidator: PublicKey
    liquidator_margin_account: PublicKey
    greeks: PublicKey
    oracle: PublicKey
    market: PublicKey
    zeta_group: PublicKey
    liquidated_margin_account: PublicKey


def liquidate(
    args: LiquidateArgs, accounts: LiquidateAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["liquidator"], is_signer=True, is_writable=False),
        AccountMeta(
            pubkey=accounts["liquidator_margin_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=accounts["greeks"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["oracle"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["market"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["liquidated_margin_account"],
            is_signer=False,
            is_writable=True,
        ),
    ]
    identifier = b"\xdf\xb3\xe2}0.'J"
    encoded_args = layout.build(
        {
            "size": args["size"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
