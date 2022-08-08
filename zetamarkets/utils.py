from anchorpy import Idl, Program, Provider
import solana
from decimal import Decimal
import math
from typing import Dict
from exchange import Exchange
from zetamarkets.constants import IDL_PATH, PLATFORM_PRECISION
from solana.publickey import PublicKey
from solana.transaction import Transaction, TransactionSignature
import solana.rpc.api

def default_commitment() -> Dict:
    return {
        "skipPreflight": False,
        "preflightCommitment": "confirmed",
        "commitment": "confirmed",
    }


def get_vault(program_id: PublicKey, zeta_group: PublicKey):
    return solana.publickey.PublicKey.find_program_address(
        [bytes("vault", "utf-8"), bytes(zeta_group)], program_id
    )


def get_serum_vault(program_id: solana.publickey.PublicKey, zeta_group):
    """_summary_

    Parameters
    ----------
    program_id : _type_
            _description_
    zeta_group : _type_
            _description_
    """
    pass


def get_mint_authority(program_id: PublicKey):
    return PublicKey.find_program_address(
        [bytes("mint-auth", "utf-8")], program_id
    )


def get_serum_authority(program_id: PublicKey):
    return PublicKey.find_program_address(
        [bytes("serum", "utf-8")], program_id
    )


def get_zeta_group(
    program_id: PublicKey, mint: PublicKey
):
    """_summary_

    Parameters
    ----------
    program_id : solana.publickey.PublicKey
            _description_
    mint : solana.publickey.PublicKey
            _description_

    Returns
    -------
    _type_
            _description_
    """
    return PublicKey.find_program_address(
        [bytes("zeta-group", "utf-8"), mint], program_id
    )


def get_zeta_vault(program_id: PublicKey, mint: PublicKey):
    pass

def get_zeta_insurance_vault(program_id: PublicKey, zeta_group_address: PublicKey):
    return PublicKey.find_program_address(
        [bytes("zeta-insurance-vault", "utf-8"), bytes(zeta_group_address)], program_id
    )

def get_socialized_loss_account(program_id: PublicKey, zeta_group_address: PublicKey):
    return PublicKey.find_program_address(
        [bytes("socialized-loss", "utf-8"), bytes(zeta_group_address)], program_id
        )





def get_user_white_list_deposit_account():
    pass


def get_state(program_id):
    return PublicKey.find_program_address(
        [bytes("state", "utf-8")], program_id
    )


def get_market_uninitialized():
    pass


def get_underlying(program_id: PublicKey, underlying_index: int):
    return solana.publickey.PublicKey.find_program_address(
        [bytes("underlying", "utf-8"), bytes([underlying_index])], program_id
    )


def convert_native_lot_size_to_decimal(amount):
    """
    Converts a native lot size where 1 unit = 0.001 lots to human readable decimal
    """
    return amount / math.pow(10, constants.POSITION_PRECISION)


def convert_decimal_to_native_integer(amount):
    return Decimal(amount)

def get_most_recent_expired_index():
    if exchange.markets.front_expiry_index - 1 < 0:
        return constants.ACTIVE_EXPIRIES -1
    else:
        return exchange.markets.front_expiry_index - 1

def display_state():
    ordered_indexes = [
        exchange._zeta_group.front_expiry_index,
        get_most_recent_expired_index()

    ]
    print("[EXCHANGE] Display market state...")


def get_margin_account(program_id: PublicKey, zeta_group: PublicKey, user_key: PublicKey):
    return solana.publickey.PublicKey.find_program_address(
        [
            bytes("margin", "utf-8"),
            bytes(zeta_group),
            bytes(user_key),
        ],
        program_id,
    )


def get_associated_token_address(mint: PublicKey, owner: PublicKey):
    # TODO(J0): Figure out how to properly import Addresses below from SPL
    return solana.publickey.PublicKey.find_program_address(
        [
            bytes(owner),
            bytes(
                solana.publickey.PublicKey(
                    "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
                )
            ),
            bytes(mint),
        ],
        solana.publickey.PublicKey("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"),
    )[0]

def get_zeta_group(program_id: PublicKey, mint: PublicKey):
    return PublicKey.find_program_address(
        [
            bytes("zeta-group", "utf-8"),
            bytes(mint),
        ],
        program_id
    )

def get_greeks(program_id: PublicKey, zeta_group: PublicKey):
    return solana.publickey.PublicKey.find_program_address(
        [
            bytes("greeks", "utf-8"),
            bytes(zeta_group),
        ],
        program_id
    )

def get_underlying(program_id: PublicKey, underlying_index: int):
    return solana.publickey.PublicKey.find_program_address(
        [
            bytes("underlying", "utf-8"),
            bytes([underlying_index]),
        ],
        program_id
    )

async def process_transaction(provider: Provider, tx: Transaction, signers=None, opts=None, use_ledger=False):
    # TODO: Implement this
    txSig = TransactionSignature()
    blockhash = await provider.connection.get_recent_blockhash()
    tx.recent_blockhash = blockhash
    tx.fee_payer = Exchange.ledger_wallet.public_key if use_ledger else provider.wallet.public_key
    if signers == None:
        signers = []
    
    for s in signers:
        if s != None:
            tx.sign_partial(s)
    
    if use_ledger:
        tx = await Exchange.ledger_wallet.sign_transaction(tx)
    else:
        tx = await provider.wallet.sign_transaction(tx)
    
    try:
        tx_sig = await solana.rpc.api.Client.send_raw_transaction(Exchange.client, tx.serialize(), opts)
