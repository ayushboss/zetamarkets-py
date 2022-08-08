from exchange import Exchange
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, Transaction
from solana.sysvar import SYSVAR_RENT_PUBKEY
from my_client.instructions import *
from solana.system_program import SYS_PROGRAM_ID
import utils
from spl.token.constants import TOKEN_PROGRAM_ID
import constants
from zetamarkets.constants import DEX_PID

def initialize_margin_account_ix(zeta_group, margin_account, user):
    return initialize_margin_account({
        "zeta_group": zeta_group,
        "margin_account": margin_account,
        "authority": user,
        "payer": user,
        "zeta_program": Exchange.program_id,
        "system_program": SYS_PROGRAM_ID
    })

def close_margin_account_ix(asset, user_key, margin_account):
    return close_margin_account({
        "margin_account": margin_account,
        "authority": user_key,
        "zeta_group": Exchange.get_zeta_group_address(asset)
    })

async def initialize_insurance_deposit_account_ix(asset, user_key, user_whitelist_insurance_key):
    sub_exchange = Exchange.get_sub_exchange(asset)
    insurance_deposit_account, nonce = await utils.get_user_white_list_deposit_account(
        Exchange.program_id,
        sub_exchange.zeta_group_address,
        user_key
    )

    return initialize_insurance_deposit_account(nonce, {
        "zeta_group": sub_exchange.zeta_group_address,
        "insurance_deposit_account": insurance_deposit_account,
        "authority": user_key,
        "system_program": SYS_PROGRAM_ID,
        "whitelist_insurance_account": user_whitelist_insurance_key
    })

async def deposit_ix(asset, amount, margin_account, usdc_account, user_key, whitelist_deposit_account):
    remaining_accounts = []
    if whitelist_deposit_account != None:
        remaining_accounts = [{
            "pubkey": whitelist_deposit_account,
            "is_signer": False,
            "is_writable": False
        }]
    
    sub_exchange = Exchange.get_sub_exchange(asset)

    return deposit(amount, {
        "zeta_group": sub_exchange.zeta_group_address,
        "margin_account": margin_account,
        "vault": sub_exchange.vault_address,
        "user_token_account": usdc_account,
        "socialized_loss_account": sub_exchange.socialized_loss_account_address,
        "authority": user_key,
        "token_program": TOKEN_PROGRAM_ID,
        "state": Exchange.state_address,
        "greeks": sub_exchange.zeta_group.greels
    })

def deposit_insurance_vault_ix(asset, amount, insurance_deposit_account, usdc_account, user_key):
    sub_exchange = Exchange.get_sub_exchange(asset)
    return deposit_insurance_vault(
        amount,
        {
            "zeta_group": sub_exchange.zeta_group_address,
            "insurance_vault": sub_exchange.insurance_vault_address,
            "insurance_deposit_account": insurance_deposit_account,
            "user_token_account": usdc_account,
            "zeta_vault": sub_exchange.vault_address,
            "socialized_loss_account": sub_exchange.socialized_loss_account_address,
            "authority": user_key,
            "token_program": TOKEN_PROGRAM_ID
        }
    )

def withdraw_insurance_vault_ix(asset, percentage_amount, insurance_deposit_account, usdc_account, user_key):
    sub_exchange = Exchange.get_sub_exchange(asset)
    return withdraw_insurance_vault(
        percentage_amount,
        {
            "zeta_group": sub_exchange.zeta_group_address,
            "insurance_vault": sub_exchange.insurance_vault_address,
            "insurance_deposit_account": insurance_deposit_account,
            "user_token_account": usdc_account,
            "authority": user_key,
            "token_program": TOKEN_PROGRAM_ID
        }
    )

def withdraw_ix(asset, amount, margin_account, usdc_account, user_key):
    sub_exchange = Exchange.get_sub_exchange(asset)
    return withdraw(
        amount,
        {
            "state": Exchange.state_address,
            "zeta_group": sub_exchange.zeta_group_address,
            "vault": sub_exchange.vault_address,
            "margin_account": margin_account,
            "user_token_account": usdc_account,
            "authority": user_key,
            "token_program": TOKEN_PROGRAM_ID,
            "greeks": sub_exchange.zeta_groups.greeks,
            "oracle": sub_exchange.zeta_group.oracle,
            "socialized_loss_account": sub_exchange.socialized_loss_account_address
        }
    )

async def initialize_open_orders_ix(asset, market, user_key, margin_account):
    open_orders_pda, _open_orders_nonce = await utils.get_open_orders(
        Exchange.program_id,
        market,
        user_key
    )

    open_orders_map, _open_orders_map_nonce = await utils.get_open_orders_map(
        Exchange.program_id,
        open_orders_pda
    )

    return [
        initialize_open_orders({
            "state": Exchange.state_address,
            "zeta_group": Exchange.get_zeta_group_address(asset),
            "dex_program": constants.DEX_PID[Exchange.network],
            "system_program": SYS_PROGRAM_ID,
            "open_orders": open_orders_pda,
            "margin_account": margin_account,
            "authority": user_key,
            "payer": user_key,
            "market": market,
            "rent": SYSVAR_RENT_PUBKEY,
            "serum_authority": Exchange._serum_authority,
            "open_orders_map": open_orders_map
        }),
        open_orders_pda
    ]

async def close_open_orders_ix(asset, market, user_key, margin_account, open_orders):
    open_orders_map, open_orders_map_nonce = await utils.get_open_orders_map(
        Exchange.program_id,
        open_orders
    )

    return close_open_orders(open_orders_map_nonce,
        {
            "state": Exchange.state_address,
            "zeta_group": Exchange.get_zeta_group_address(asset),
            "dex_program": constants.DEX_PID[Exchange.network],
            "open_orders": open_orders,
            "margin_account": margin_account,
            "authority": user_key,
            "market": market,
            "serum_authority": Exchange._serum_authority,
            "open_orders_map": open_orders_map
        }
    )

def place_order_ix(asset, market_index, price, size, side, client_order_id, margin_account, authority, open_orders, whitelist_trading_fees_account):
    sub_exchange = Exchange.get_sub_exchange(asset)
    market_data = sub_exchange.markets.markets[market_index]
    remaining_accounts = []
    if whitelist_trading_fees_account != None:
        remaining_accounts == [{
            "pubkey": whitelist_trading_fees_account,
            "is_signer": False,
            "is_writable": False
        }]
    
    return place_order(
        price,
        size,
        types.to_program_side(side),
        None if client_order_id == 0 else client_order_id,
        {
            "state": Exchange.state_address,
            "zeta_group": sub_exchange.zeta_group_address,
            "margin_account": margin_account,
            "authority": authority,
            "dex_program": constants.DEX_PID[Exchange.network],
            "token_program": TOKEN_PROGRAM_ID,
            "serum_authority": Exchange._serum_authority,
            "greeks": sub_exchange.zeta_group.greeks,
            "open_orders": open_orders,
            "rent": SYSVAR_RENT_PUBKEY,
            "market_accounts": {
                "market": market_data.serum_market.decoded.own_address,
                "request_queue": market_data.serum_market.decoded.request_queue,
                "event_queue": market_data.serum_market.decoded.event_queue,
                "bids": market_data.serum_market.decoded.bids,
                "asks": market_data.serum_market.decoded.asks,
                "coin_vault": market_data.serum_market.decoded.base_vault,
                "pc_vault": market_data.serum_market.decoded.quote_vault,
                "order_payer_token_account": market_data.base_vault if side == types.Side.BID else market_data.base_vault,
                "coin_wallet": market_data.base_vault,
                "pc_wallet": market_data.quote_vault
            },
            "oracle": sub_exchange.zeta_group.oracle,
            "market_node": sub_exchange.greeks.node_keys[market_index],
            "market_mint": market_data.serum_market.quote_mint_address if side == types.Side.BID else market_data.serum_market.base_mint_address,
            "mint_authority": Exchange._mint_authority
        },
        remaining_accounts
    )

def initialize_zeta_state_ix(state_address, state_nonce, serum_authority, treasury_wallet, serum_nonce, mint_authority, mint_authority_nonce, params):
    args = params
    args["state_nonce"] = state_nonce
    args["serum_nonce"] = serum_nonce
    args["mint_auth_nonce"] = mint_authority_nonce

    return initialize_zeta_state(
        args,
        {
            "state": state_address,
            "serum_authority": serum_authority,
            "mint_authority": mint_authority,
            "treasury_wallet": treasury_wallet,
            "rent": SYSVAR_RENT_PUBKEY,
            "system_program": SYS_PROGRAM_ID,
            "usdc_mint": Exchange._usdc_mint_address,
            "admin": Exchange.provider.wallet.publicKey
        }
    )

async def intialize_zeta_group_ix(asset, underlying_mint, oracle, pricing_args, margin_args):
    zeta_group, zeta_group_nonce = await utils.get_zeta_group(
        Exchange.program_id,
        underlying_mint
    )

    underlying, underlying_nonce = await utils.get_underlying(
        Exchange.program_id,
        Exchange._state.num_underlyings
    )

    sub_exchange = Exchange.get_sub_exchange(asset)

    greeks, greeks_nonce = await utils.get_greeks(
        Exchange.program_id,
        sub_exchange.zeta_group_address
    )

    vault, vault_nonce = await utils.get_vault(
        Exchange.program_id,
        sub_exchange.zeta_group_address
    )

    insurance_vault, insurance_vault_nonce = await utils.get_zeta_insurance_vault(
        Exchange.program_id,
        sub_exchange.zeta_group_address
    )

    socialized_loss_account, socialized_loss_account_nonce = await utils.get_socialized_loss_account(
        Exchange.program_id,
        sub_exchange.zeta_group_address
    )

    return initialize_zeta_group(
        {
            "zeta_group_nonce": zeta_group_nonce,
            "underlying_nonce": underlying_nonce,
            "greeks_nonce": greeks_nonce,
            "vault_nonce": vault_nonce,
            "insurance_vault_nonce": insurance_vault_nonce,
            "socialized_loss_account_nonce": socialized_loss_account_nonce,
            "interest_rate": pricing_args.interest_rate,
            "volatility": pricing_args.volatility,
            "option_trade_normalizer": pricing_args.option_trade_normalizer,
            "future_trade_normalizer": pricing_args.future_trade_normalizer,
            "max_volatility_retreat": pricing_args.max_volatility_retreat,
            "max_interest_retreat": pricing_args.max_interest_retreat,
            "max_delta": pricing_args.max_delta,
            "min_delta": pricing_args.min_delta,
            "min_interest_rate": pricing_args.min_interest_rate,
            "max_interest_rate": pricing_args.max_interest_rate,
            "min_volatility": pricing_args.min_volatility,
            "max_volatility": pricing_args.max_volatility,
            "future_margin_initial": margin_args.future_margin_initial,
            "future_margin_maintenance": margin_args.future_margin_maintenance,
            "option_mark_percentage_long_initial": margin_args.option_mark_percentage_long_initial,
            "option_spot_percentage_long_initial": margin_args.option_spot_percentage_long_initial,
            "option_spot_percentage_short_initial": margin_args.option_spot_percentage_short_initial,
            "option_dynamic_percentage_short_initial": margin_args.option_dynamic_percentage_short_initial,
            "option_mark_percentage_long_maintenance": margin_args.option_mark_percentage_long_maintenance,
            "option_spot_percentage_long_maintenance": margin_args.option_spot_percentage_long_maintenance,
            "option_spot_percentage_short_maintenance": margin_args.option_spot_percentage_short_maintenance,
            "option_dynamic_percentage_short_maintenance": margin_args.option_dynamic_percentage_short_maintenance,
            "option_short_put_cap_percentage": margin_args.option_short_put_cap_percentage,
        },
        {
            "state": Exchange.state_address,
            "admin": Exchange.state.admin,
            "system_program": SYS_PROGRAM_ID,
            "underlying_mint": underlying_mint,
            "zeta_program": Exchange.program_id,
            "oracle": oracle,
            "zeta_group": zeta_group,
            "greeks": greeks,
            "underlying": underlying,
            "vault": vault,
            "insurance_vault": insurance_vault,
            "socialized_loss_account": socialized_loss_account,
            "token_program": TOKEN_PROGRAM_ID,
            "usdc_mint": Exchange._usdc_mint_address,
            "rent": SYSVAR_RENT_PUBKEY,
        }
    )

def update_zeta_state_ix(params, admin):
    return update_zeta_state(params, {
        {
            "state": Exchange.state_address,
            "admin": admin
        }
    })

async def initialize_referrer_alias(referrer, alias):
    referrer_account = await utils.get_referrer_account_address(
        Exchange.program.program_id,
        referrer
    )

    referrer_alias = await utils.get_referrer_alias_address(
        Exchange.program.program_id,
        alias
    );

    return initialize_referrer_alias(alias, {
        {
            "referrer": referrer,
            "referrer_alias": referrer_alias,
            "referrer_account": referrer_account,
            "system_program": SYS_PROGRAM_ID,
        },
    });