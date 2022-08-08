from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class SettlePositionsArgs(typing.TypedDict):
    expiry_ts: int
    settlement_nonce: int


layout = borsh.CStruct("expiry_ts" / borsh.U64, "settlement_nonce" / borsh.U8)


class SettlePositionsAccounts(typing.TypedDict):
    zeta_group: PublicKey
    settlement_account: PublicKey


def settle_positions(
    args: SettlePositionsArgs, accounts: SettlePositionsAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["settlement_account"], is_signer=False, is_writable=False
        ),
    ]
    identifier = b"+B\xc8\xd8\xdb\xba,W"
    encoded_args = layout.build(
        {
            "expiry_ts": args["expiry_ts"],
            "settlement_nonce": args["settlement_nonce"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
