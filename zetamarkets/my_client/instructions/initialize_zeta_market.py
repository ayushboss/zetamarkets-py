from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class InitializeZetaMarketArgs(typing.TypedDict):
    args: types.initialize_market_args.InitializeMarketArgs


layout = borsh.CStruct(
    "args" / types.initialize_market_args.InitializeMarketArgs.layout
)


class InitializeZetaMarketAccounts(typing.TypedDict):
    state: PublicKey
    market_indexes: PublicKey
    zeta_group: PublicKey
    admin: PublicKey
    market: PublicKey
    request_queue: PublicKey
    event_queue: PublicKey
    bids: PublicKey
    asks: PublicKey
    base_mint: PublicKey
    quote_mint: PublicKey
    zeta_base_vault: PublicKey
    zeta_quote_vault: PublicKey
    dex_base_vault: PublicKey
    dex_quote_vault: PublicKey
    vault_owner: PublicKey
    mint_authority: PublicKey
    serum_authority: PublicKey
    dex_program: PublicKey
    system_program: PublicKey
    token_program: PublicKey
    rent: PublicKey


def initialize_zeta_market(
    args: InitializeZetaMarketArgs, accounts: InitializeZetaMarketAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["market_indexes"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["market"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["request_queue"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["event_queue"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["bids"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["asks"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["base_mint"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["quote_mint"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["zeta_base_vault"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["zeta_quote_vault"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["dex_base_vault"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["dex_quote_vault"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["vault_owner"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["mint_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["serum_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["dex_program"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["rent"], is_signer=False, is_writable=False),
    ]
    identifier = b"t\xef\xe2\x95.\xa3\xdd\x03"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
