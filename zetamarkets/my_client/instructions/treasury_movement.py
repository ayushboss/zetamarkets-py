from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class TreasuryMovementArgs(typing.TypedDict):
    treasury_movement_type: types.treasury_movement_type.TreasuryMovementTypeKind
    amount: int


layout = borsh.CStruct(
    "treasury_movement_type" / types.treasury_movement_type.layout, "amount" / borsh.U64
)


class TreasuryMovementAccounts(typing.TypedDict):
    state: PublicKey
    zeta_group: PublicKey
    insurance_vault: PublicKey
    treasury_wallet: PublicKey
    token_program: PublicKey
    admin: PublicKey


def treasury_movement(
    args: TreasuryMovementArgs, accounts: TreasuryMovementAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["insurance_vault"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["treasury_wallet"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
    ]
    identifier = b'\x01"\xf2i\xd7\xd3\x9d\x12'
    encoded_args = layout.build(
        {
            "treasury_movement_type": args["treasury_movement_type"].to_encodable(),
            "amount": args["amount"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
