from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class InitializeZetaGroupArgs(typing.TypedDict):
    args: types.initialize_zeta_group_args.InitializeZetaGroupArgs


layout = borsh.CStruct(
    "args" / types.initialize_zeta_group_args.InitializeZetaGroupArgs.layout
)


class InitializeZetaGroupAccounts(typing.TypedDict):
    state: PublicKey
    admin: PublicKey
    system_program: PublicKey
    underlying_mint: PublicKey
    zeta_program: PublicKey
    oracle: PublicKey
    zeta_group: PublicKey
    greeks: PublicKey
    underlying: PublicKey
    vault: PublicKey
    insurance_vault: PublicKey
    socialized_loss_account: PublicKey
    token_program: PublicKey
    usdc_mint: PublicKey
    rent: PublicKey


def initialize_zeta_group(
    args: InitializeZetaGroupArgs, accounts: InitializeZetaGroupAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=True),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["underlying_mint"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["zeta_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["oracle"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["greeks"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["underlying"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["vault"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["insurance_vault"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["socialized_loss_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["usdc_mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["rent"], is_signer=False, is_writable=False),
    ]
    identifier = b"\x06\x87$\xe8#'\xfaG"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
