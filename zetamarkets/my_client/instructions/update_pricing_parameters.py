from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class UpdatePricingParametersArgs(typing.TypedDict):
    args: types.update_pricing_parameters_args.UpdatePricingParametersArgs


layout = borsh.CStruct(
    "args" / types.update_pricing_parameters_args.UpdatePricingParametersArgs.layout
)


class UpdatePricingParametersAccounts(typing.TypedDict):
    state: PublicKey
    zeta_group: PublicKey
    admin: PublicKey


def update_pricing_parameters(
    args: UpdatePricingParametersArgs, accounts: UpdatePricingParametersAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
    ]
    identifier = b"i\x7f\xd0\x86==q\xf7"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
