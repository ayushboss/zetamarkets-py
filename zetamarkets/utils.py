from anchorpy import Idl, Program
import solana
from decimal import Decimal
import math
from typing import Dict
from zetamarkets import constants, exchange


def default_commitment() -> Dict:
    return {
        "skipPreflight": False,
        "preflightCommitment": "confirmed",
        "commitment": "confirmed",
    }


def get_vault(program_id, zeta_group):
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


def get_mint_authority(program_id: solana.publickey.PublicKey):
    return solana.publickey.PublicKey.find_program_address(
        [bytes("mint-auth", "utf-8")], program_id
    )


def get_serum_authority(program_id: solana.publickey.PublicKey):
    return solana.publickey.PublicKey.find_program_address(
        [bytes("serum", "utf-8")], program_id
    )


def get_zeta_group(
    program_id: solana.publickey.PublicKey, mint: solana.publickey.PublicKey
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
    return solana.publickey.PublicKey.find_program_address(
        [bytes("zeta-group", "utf-8"), mint], program_id
    )


def get_zeta_vault(program_id, mint):
    pass


def get_user_white_list_deposit_account():
    pass


def get_state(program_id):
    return solana.publickey.PublicKey.find_program_address(
        [bytes("state", "utf-8")], program_id
    )


def get_market_uninitialized():
    pass


def get_underlying(program_id, underlying_index: int):
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


def display_state():
    print(exchange.Exchange().zetagroup)
