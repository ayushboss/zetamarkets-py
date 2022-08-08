from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class InitializeZetaStateArgs(typing.TypedDict):
    args: types.initialize_state_args.InitializeStateArgs


layout = borsh.CStruct("args" / types.initialize_state_args.InitializeStateArgs.layout)


class InitializeZetaStateAccounts(typing.TypedDict):
    state: PublicKey
    mint_authority: PublicKey
    serum_authority: PublicKey
    treasury_wallet: PublicKey
    rent: PublicKey
    system_program: PublicKey
    token_program: PublicKey
    usdc_mint: PublicKey
    admin: PublicKey


def initialize_zeta_state(
    args: InitializeZetaStateArgs, accounts: InitializeZetaStateAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["mint_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["serum_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["treasury_wallet"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["rent"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["usdc_mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=True),
    ]
    identifier = b"D'K\x8e\xbf\x92^\xde"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
