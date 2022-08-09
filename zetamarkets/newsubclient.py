from ctypes.wintypes import tagMSG
from datetime import datetime
from re import M
import string
from this import d

import anchorpy
from exchange import Exchange
from solana.publickey import PublicKey
from solana.transaction import Transaction
import constants
import utils
from zetamarkets.assets import Asset
from zetamarkets.newclient import Client
import program_instructions as instructions
import var_types as types

import solana

class SubClient:
    @property
    def margin_account(self):
        return self._margin_account
    
    @property
    def margin_account_address(self):
        return self._margin_account_address
    
    @property
    def asset(self):
        return self._asset
    
    @property
    def parent(self):
        return self._parent

    @property
    def sub_exchange(self):
        return self._sub_exchange
    
    @property
    def spread_account(self):
        return self._spread_account
    
    @property
    def spread_account_address(self):
        return self._spread_account_address
    
    @property
    def open_orders_accounts(self):
        return self._open_orders_accounts
    
    @property
    def orders(self):
        return self._orders
    
    @property
    def margin_positions(self):
        return self._margin_positions
    
    @property
    def spread_positions(self):
        return self._spread_positions
    
    @property
    def poll_interval(self):
        return self._poll_interval
    
    def set_poll_interval(self, interval):
        if interval < 0:
            raise Exception("Polling interval invalid!")
        self._poll_interval = interval
    
    def __init__(self, asset, parent: Client):
        self._asset = asset
        self._sub_exchange = Exchange.get_sub_exchange(asset)
        self._open_orders_accounts = []
        for i in range(len(self._sub_exchange.zeta_group.products)):
            self._open_orders_accounts.append(PublicKey(0))
        self._parent = parent

        self._margin_positions = []
        self._spread_positions = []
        self._orders = []
        self._last_update_timestamp = 0
        self._pending_update = False
        self._margin_account = None
        self._margin_account_address = None
        self._spread_account = None
        self._poll_interval = constants.DEFAULT_CLIENT_POLL_INTERVAL
        self._updating_state = False
        self._updating_state_timestamp = None
        self._spread_account_address = None
        self._callback = None
    
    async def load(self, asset: Asset, parent: Client, connection, wallet: anchorpy.Wallet, callback = None, throttle: bool = False):
        subClient = SubClient(asset, parent)
        margin_account_address, _margin_account_nonce = await utils.get_margin_account(
            Exchange.program_id,
            subClient._sub_exchange.zeta_group_address,
            wallet.public_key()
        )

        spread_account_address, _spread_account_nonce = await utils.get_spread_account(
            Exchange.program_id,
            subClient._sub_exchange.zeta_group_address,
            wallet.public_key()
        )

        subClient._margin_account_address = margin_account_address
        subClient._spread_account_address = spread_account_address

        subClient._callback = callback

        ### TODO: NEED TO FIGURE THIS OUT
        # subClient._margin_account_subscription_id = connection.on_account_change(
        #     subClient._margin_account_address,
        # )



        ### TODO: NEED TO FIGURE THIS OUT TOO
        # subClient._spread_account_subscription_id = connection.on_account_change(

        # )

        try:
            subClient._margin_account = await Exchange.program.account.margin_account.fetch(
                subClient._margin_account_address
            )

            await subClient.update_open_order_addresses()
            subClient.update_margin_positions()

            subClient._pending_update = True
        except:
            raise Exception("User does not have a margin account.")

        try:
            subClient._spread_account = await Exchange.program.account.spread_account.fetch(
                subClient._spread_account_address
            )
            subClient.update_spread_positions()
        except:
            raise Exception("User does not have a spread account.")
        
        ### TODO: NEED TO FIGURE OUT HOW TO IMPLEMENT CALLBACK FUNCTION FUNCTIONALITY

        # if callback != None:
        #     subClient._trade_event_listener = Exchange.program.add_event_listener(
        #         "TradeEvent",
                
        #     )

    async def poll_update(self):
        if Exchange.clock_timestamp > self._last_update_timestamp + self._poll_interval or self._pending_update:
            try:
                if self._updating_state:
                    return
                latest_slot = self._pending_update_slot
                await self.update_state()

                if latest_slot == self._pending_update_slot:
                    self._pending__update = False
                
                self._last_update_timestamp = Exchange.clock_timestamp
                if self._callback != None:
                    self._callback(self.asset, EventType.USER, None)
            except:
                raise Exception("Subclient poll update failed.")
    
    def toggle_update_state(self, toggle_on: bool):
        if toggle_on:
            self._updating_state = True
            self._updating_state_timestamp = datetime.now()
        else:
            self._updating_state = False
            self._updating_state_timestamp = None
    
    def check_reset_updating_state(self):
        if self._updating_state and datetime.now() - self._updating_state_timestamp > constants.UPDATING_STATE_LIMIT_SECONDS:
            self.toggle_update_state(False)
    
    async def update_state(self, fetch: bool = True, force: bool = False):
        self.check_reset_updating_state()
        if self._updating_state and not force:
            return
        self.toggle_update_state(True)

        if fetch:
            try:
                self._margin_account = await Exchange.program.account.marginAccount.fetch(
                    self._margin_account_address
                )
            except:
                self.toggle_update_state(False)
                return
            
            try:
                self._spread_account = await Exchange.program.account.spreadAccount.fetch(
                    self._spread_account_address
                )
            except:
                print("Some error")
        
        try:
            if self._margin_account == None:
                self.update_margin_positions()
                await self.update_orders()
            if self._spread_account != None:
                self.update_spread_positions()
        except:
            print("Some error 2")
        
        self.toggle_update_state(False)
    
    async def deposit(self, amount: int):
        tx = Transaction()
        if self._margin_account == None:
            print("User has no margin account. Creating margin account...")
            tx.add(
                instructions.initialize_margin_account_ix(
                    self._sub_exchange.zeta_group_address,
                    self._margin_account_address,
                    self._parent.public_key()
                )
            )
        tx.add(
            await instructions.deposit_ix(
                self.asset,
                amount,
                self._margin_account_address,
                self._parent.usdc_account_address,
                self._parent.public_key(),
                self._parent.whitelist_deposit_address
            )
        )

        txId = await utils.process_transaction(self._parent.provider, tx)
        return txId
    
    async def close_margin_account(self):
        if self._margin_account == None:
            raise Exception("User has no margin account to close")
        tx = Transaction().add(
            instructions.close_margin_account_ix(
                self.asset,
                self._parent.public_key(),
                self._margin_account_address
            )
        )
        txId = await utils.process_transaction(self._parent.provider, tx)
        self._margin_account = None
        return txId
    
    async def close_spread_account(self):
        if self._spread_account == None:
            raise Excpetion("User has no spread account to close")

        sub_exchange = self._sub_exchange
        tx = Transaction()
        tx.add(
            instructions.transfer_excess_spread_balance_ix(
                sub_exchange.zeta_group_address,
                self._margin_account_address,
                self._spread_account_address,
                self._parent.public_key()
            )
        )
        tx.add(
            instructions.close_spread_account_ix(
                self.asset,
                self._parent.public_key(),
                self._spread_account_address
            )
        )
        txId = await utils.process_transaction(self._parent.provider, tx)
        self._spread_account = None
        return txId
    
    async def withdraw(self, amount: int):
        tx = Transaction()
        tx.add(
            instructions.withdraw_ix(
                self.asset,
                amount,
                self._margin_account_address,
                self._parent.usdc_account_address,
                self._parent.public_key()
            )
        )
        return await utils.process_transaction(self._parent.provider, tx)
    
    async def withdraw_and_close_margin_account(self):
        if self._margin_account == None:
            raise Exception("User has no margin account to withdraw or close.")
        tx = Transaction()
        tx.add(
            instructions.withdraw_ix(
                self.asset,
                self._margin_account.balance,
                self._margin_account_address,
                self._parent.usdc_account_address,
                self._parent.public_key()
            )
        )
        tx.add(
            instructions.close_margin_account_ix(
                self.asset,
                self._parent.public_key(),
                self.margin_account_address
            )
        )
        return await utils.process_transaction(self._parent.provider, tx)
    
    async def place_order(self, market, price, size, side, client_order_id):
        tx = Transaction()
        market_index = self._sub_exchange.markets.get_market_index(market)
        
        open_orders_pda = None
        if self._open_orders_accounts[market_index] == PublicKey(0):
            print("User doesn't have open orders account. Initialising for market " + str(market))
        
            init_ix, _open_orders_pda = await instructions.initialize_open_orders_ix(
                self.asset,
                market,
                self._parent.public_key(),
                self._margin_account_address
            )

            open_orders_pda = _open_orders_pda
            tx.add(init_ix)
        else:
            open_orders_pda = self._open_orders_accounts[market_index]
        
        order_ix = await instructions.place_order_ix(
            self.asset,
            market_index,
            price,
            size,
            side,
            client_order_id,
            self._margin_account_address,
            self._parent.public_key(),
            open_orders_pda,
            self._parent.whitelist_trading_fees_address
        )

        tx.add(order_ix)

        txId = await utils.process_transaction(self._parent.provider, tx)
        self._open_orders_accounts[market_index] = open_orders_pda

        return txId
    
    async def place_order_v2(self, market, price, size, side, order_type, client_order_id = 0):
        tx = Transaction()
        market_index = self._sub_exchange.markets.get_market_index(market)

        open_orders_pda = None
        if self._open_orders_accounts[market_index] == PublicKey(0):
            print("User doesn't have open orders account. Initialising for market: " + str(market))
            init_ix, _open_orders_pda = await instructions.initialize_open_orders_ix(
                self.asset,
                market,
                self._parent.public_key(),
                self._margin_account_address
            )
            open_orders_pda = _open_orders_pda
            tx.add(init_ix)
        else:
            open_orders_pda = self._open_orders_accounts[market_index]
        
        order_ix = instructions.place_order_v2_ix(
            self.asset,
            market_index,
            price,
            size,
            side,
            order_type,
            client_order_id,
            self._margin_account_address,
            self._parent.public_key(),
            open_orders_pda,
            self._parent.whitelist_trading_fees_address
        )

        tx.add(order_ix)

        txId = await utils.process_transaction(self._parent.provider, tx)
        self._open_orders_accounts[market_index] = open_orders_pda
    
    async def place_order_and_lock_position(self, market, price, size, side, tag):
        tx = Transaction()
        sub_exchange = self._sub_exchange
        market_index = sub_exchange.markets.get_market_index(market)

        open_orders_pda = None
        if self._open_orders_accounts[market_index] == PublicKey(0):
            print("User doesn't have open orders account. Initializing for market: " + str(market))
            init_ix, _open_orders_pda = await instructions.initialize_open_orders_ix(
                self.asset,
                market,
                self._parent.public_key(),
                self._margin_account_address
            )
            open_orders_pda = _open_orders_pda
            tx.add(init_ix)
        else:
            open_orders_pda = self._open_orders_accounts[market_index]
        
        order_ix = instructions.place_order_v3_ix(
            self.asset,
            market_index,
            price,
            size,
            side,
            types.OrderType.FILLORKILL,
            0,
            tag,
            self._margin_account_address,
            self._parent.public_key(),
            open_orders_pda,
            self._parent.whitelist_trading_fees_address
        )

        tx.add(order_ix)

        if self.spread_account == None:
            print("User has no spread account. Creating spread account")
            tx.add(
                instructions.initialize_spread_account_ix(
                    sub_exchange.zeta_group_address,
                    self.spread_account_address,
                    self._parent.public_key()
                )
            )
        movement_size = None
        if side == types.Side.BID:
            movement_size = size
        else:
            movement_size = -size

        movements = [{
            index: market_index,
            size: movement_size
        }]

        tx.add(
            instructions.position_movement_ix(
                sub_exchange.zeta_group_address,
                self._margin_account_address,
                self.spread_account_address,
                self._parent.public_key(),
                sub_exchange.greeks_address,
                sub_exchange.zeta_group.oracle,
                types.MovementType.LOCK,
                movements
            )
        )

        txId = await utils.process_transaction(self._parent.provider, tx)
        self._open_orders_accounts[market_index] = open_orders_pda

        return txId

    async def place_order_v3(self, market, price, size, side, order_type, client_order_id, tag):
        tx = Transaction()
        market_index = self._sub_exchange.markets.get_market_index(market)

        open_orders_pda = None
        if self._open_orders_accounts[market_index] == PublicKey(0):
            print("User doesn't have open orders account for this asset. Initializing for market: " + str(market))
            init_ix, _open_orders_pda = await instructions.initialize_open_orders_ix(
                self.asset,
                market,
                self._parent.public_key(),
                self._margin_account_address
            )
            open_orders_pda = _open_orders_pda
            tx.add(init_ix)
        else:
            open_orders_pda = self._open_orders_accounts[market_index]

        order_ix = instructions.place_order_v3_ix(
            self.asset,
            market_index,
            price,
            size,
            side,
            order_type,
            client_order_id,
            tag,
            self._margin_account_address,
            self._parent.public_key(),
            open_orders_pda,
            self._parent.whitelist_trading_fees_address
        )

        tx.add(order_ix)

        txId = await utils.process_transaction(self._parent.provider, tx)
        self._open_orders_accounts[market_index] = open_orders_pda
        return txId
    
    async def cancel_order(self, market, order_id, side):
        tx = Transaction()
        index = self._sub_exchange.markets.get_market_index(market)
        ix = instructions.cancel_order_ix(
            self.asset,
            index,
            self._parent.public_key(),
            self._margin_account_address,
            self._open_orders_accounts[index],
            order_id,
            side
        )
        tx.add(ix)
        return await utils.process_transaction(self._parent.provider, tx)
    
    async def cancel_order_by_client_order_id(self, market, client_order_id):
        if client_order_id == 0:
            raise Exception("SubClient order id cannot be 0")
        tx = Transaction()
        index = self._sub_exchange.markets.get_market_index(market)
        ix = instructions.cancel_order_by_client_order_id_ix(
            self.asset,
            index,
            self._parent.public_key(),
            self._margin_account_address,
            self._open_orders_accounts[index],
            client_order_id
        )

        tx.add(ix)
        return await utils.process_transaction(self._parent.provider, tx)
    
    async def cancel_and_place_order(self, market, order_id, cancel_side, new_order_price, new_order_size, new_order_side, client_order_id):
        tx = Transaction()
        market_index = self._sub_exchange.markets.get_market_index(market)
        tx.add(
            instructions.cancel_order_ix(
                self.asset,
                market_index,
                self._parent.public_key(),
                self._margin_account_address,
                self._open_orders_accounts[market_index],
                order_id,
                cancel_side
            )
        )
        tx.add(
            instructions.place_order_ix(
                self.asset,
                market_index,
                new_order_price,
                new_order_size,
                new_order_side,
                client_order_id,
                self._margin_account_address,
                self._parent.public_key(),
                self._open_orders_accounts[market_index],
                self._parent.whitelist_trading_fees_address
            )
        )

        return await utils.process_transaction(self._parent.provider, tx)
    
    async def cancel_and_place_order_v2(self, market, order_id, cancel_side, new_order_price, new_order_size, new_order_side, new_order_type, client_order_id):
        tx = Transaction()
        market_index = self._sub_exchange.markets.get_market_index(market)
        tx.add(
            instructions.cancel_order_ix(
                self.asset,
                market_index,
                self._parent.public_key(),
                self._margin_account_address,
                self._open_orders_accounts[market_index],
                order_id,
                cancel_side
            )
        )
        tx.add(
            instructions.place_order_v2_ix(
                self.asset,
                market_index,
                new_order_price,
                new_order_size,
                new_order_side,
                new_order_type,
                client_order_id,
                self._margin_account_address,
                self._parent.public_key(),
                self._open_orders_accounts[market_index],
                self._parent.whitelist_trading_fees_address
            )
        )
        return await utils.process_transaction(self._parent.provider, tx)

    async def cancel_and_place_order_v3(self, market, order_id, cancel_side, new_order_price, new_order_size, new_order_side, new_order_type, client_order_id, new_order_tag):
        tx = Transaction()
        market_index = self._sub_exchange.markets.get_market_index(market)
        tx.add(
            instructions.cancel_order_ix(
                self.asset,
                market_index,
                self._parent.public_key(),
                self._margin_account_address,
                self._open_orders_accounts[market_index],
                order_id,
                cancel_side
            )
        )
        tx.add(
            instructions.place_order_v3_ix(
                self.asset,
                market_index,
                new_order_price,
                new_order_size,
                new_order_side,
                new_order_type,
                client_order_id,
                new_order_tag,
                self.margin_account_address,
                self._parent.public_key(),
                self._open_orders_accounts[market_index],
                self._parent.whitelist_trading_fees_address
            )
        )
        return await utils.process_transaction(self._parent.provider, tx)
    
    async def cancel_and_place_order_by_client_order_id(self, market, cancel_client_order_id, new_order_price, new_order_size, new_order_side, new_order_client_order_id):
        tx = Transaction()       
        market_index = self._sub_exchange.markets.get_market_index(market)
        tx.add(
            instructions.cancel_order_by_client_order_id_ix(
                self.asset,
                market_index,
                self._parent.public_key(),
                self._margin_account_address,
                self._open_orders_accounts[market_index],
                cancel_client_order_id
            )
        )
        tx.add(
            instructions.place_order_ix(
                self.asset,
                market_index,
                new_order_price,
                new_order_size,
                new_order_side,
                new_order_client_order_id,
                self.margin_account_address,
                self._parent.public_key(),
                self._open_orders_accounts[market_index],
                self._parent.whitelist_trading_fees_address
            )
        )
        return await utils.process_transaction(self._parent.provider, tx)
    
    async def cancel_and_place_order_by_client_order_id_v2(self, market, cancel_client_order_id, new_order_price, new_order_size, new_order_side, new_order_type, new_order_client_order_id):
        tx = Transaction()
        market_index = self._sub_exchange.markets.get_market_index(market)
        tx.add(
            instructions.cancel_order_by_client_order_id_ix(
                self.asset,
                market_index,
                self._parent.public_key(),
                self._margin_account_address,
                self._open_orders_accounts[market_index],
                cancel_client_order_id
            )
        )
        tx.add(
            instructions.place_order_v2_ix(
                self.asset,
                market_index,
                new_order_price,
                new_order_size,
                new_order_side,
                new_order_type,
                new_order_client_order_id,
                self.margin_account_address,
                self._parent.public_key(),
                self._open_orders_accounts[market_index],
                self._parent.whitelist_trading_fees_address
            )
        )
        return await utils.process_transaction(self._parent.provider, tx)

    
    async def cancel_and_place_order_by_client_order_id_v3(self, market: PublicKey, cancel_client_order_id, new_order_price, new_order_size, new_order_side, new_order_type, new_order_client_order_id: string = constants.DEFAULT_ORDER_TAG):
        tx = Transaction()
        market_index = self._sub_exchange.markets.get_market_index(market)
        tx.add(
            instructions.cancel_order_by_client_order_id_ix(
                self.asset,
                market_index,
                self._parent.public_key(),
                self._margin_account_address,
                self._open_orders_accounts[market_index],
                cancel_client_order_id
            )
        )
        tx.add(
            instructions.place_order_v3_ix(
                self.asset,
                market_index,
                new_order_price,
                new_order_size,
                new_order_side,
                new_order_type,
                new_order_client_order_id,
                self.margin_account_address,
                self._parent.public_key(),
                self._open_orders_accounts[market_index],
                self._parent.whitelist_trading_fees_address
            )
        )
        return await utils.process_transaction(self._parent.provider, tx)
    
    async def replace_by_client_order_id_v3(self, market, cancel_client_order_id, new_order_price, new_order_size, new_order_side, new_order_type, new_order_client_order_id, new_order_tag):
        tx = Transaction()
        market_index = self._sub_exchange.markets.get_market_index(market)

        tx.add(
            instructions.cancel_order_by_client_order_id_no_error_ix(
                self.asset,
                market_index,
                self._parent.public_key(),
                self._margin_account_address,
                self._open_orders_accounts[market_index],
                cancel_client_order_id
            )
        )
        tx.add(
            instructions.place_order_v3_ix(
                self.asset,
                market_index,
                new_order_price,
                new_order_size,
                new_order_side,
                new_order_type,
                new_order_client_order_id,
                new_order_tag,
                self.margin_account_address,
                self._parent.public_key(),
                self._open_orders_accounts[market_index],
                self._parent.whitelist_trading_fees_address
            )
        )
        return await utils.process_transaction(self._parent.provider, tx)
    
    async def initialize_open_orders_account(self, market):
        market_index = self._sub_exchange.markets.get_market_index(market)
        if self._open_orders_accounts[market_index] != PublicKey(0):
            raise Exception("User already has an open orders account for market")
        
        init_ix, open_orders_pda = await instructions.initialize_open_orders_ix(
            self.asset,
            market,
            self._parent.public_key(),
            self.margin_account_address
        )

        tx = Transaction().add(init_ix)
        txId = await utils.process_transaction(self._parent.provider, tx)
        self._open_orders_accounts[market_index] = open_orders_pda
        return txId
    
    async def close_open_orders_account(self, market):
        market_index = self._sub_exchange.markets.get_market_index(market)
        if self._open_orders_accounts[market_index] == PublicKey(0):
            raise Exception("User has no open orders account for this market!")
        
        vault_owner, _vault_signer_nonce = await utils.get_serum_vault_owner_and_nonce(
            market,
            constants.DEX_PID[Exchange.network]
        )

        tx = Transaction()
        tx.add(
            instructions.settle_dex_funds_ix(
                self.asset,
                market,
                vault_owner,
                self._open_orders_accounts[market_index]
            )
        )

        tx.add(
            await instructions.close_open_orders_ix(
                self.asset,
                market,
                self._parent.public_key(),
                self.margin_account_address,
                self._open_orders_accounts[market_index]
            )
        )

        txId = await utils.process_transaction(self._parent.provider, tx)
        self._open_orders_accounts[market_index] = PublicKey(0)
        return txId
    
    async def close_multiple_open_orders_account(self, markets):
        combined_ixs = []
        sub_exchange = self._sub_exchange
        for i in range(len(markets)):
            market = markets[i]
            market_index = sub_exchange.markets.get_market_index(market)
            if self._open_orders_accounts[market_index] == PublicKey(0):
                raise Exception("User has no open orders account for this market!")
            vault_owner, _vault_signer_nonce = await utils.get_serum_vault_owner_and_nonce(
                market,
                constants.DEX_PID[Exchange.network]
            )
            settle_ix = instructions.settle_dex_funds_ix(
                self.asset,
                market,
                vault_owner,
                self._open_orders_accounts[market_index]
            )
            close_ix = await instructions.close_open_orders_ix(
                self.asset,
                market,
                self._parent.public_key(),
                self.margin_account_address,
                self._open_orders_accounts[market_index]
            )
            combined_ixs.append(settle_ix)
            combined_ixs.append(close_ix)
        
        txIds = []
        combined_txs = utils.split_ixs_into_tx(
            combined_txs,
            constants.MAX_SETTLE_AND_CLOSE_PER_TX
        )

        for tx in combined_txs:
            txIds.append(await utils.process_transaction(self._parent.provider, tx))
        
        for i in range(len(markets)):
            market = markets[i]
            market_index = sub_exchange.markets.get_market_index(market)
            self._open_orders_accounts[market_index] = PublicKey(0)
        
        return txIds
    
    async def cancel_multiple_orders(self, cancel_arguments):
        ixs = []
        for i in range(len(cancel_arguments)):
            market_index = self._sub_exchange.markets.get_market_index(
                cancel_arguments[i].market
            )
            ix = instructions.cancel_order_ix(
                self.asset,
                market_index,
                self._parent.public_key(),
                self._margin_account_address,
                self._open_orders_accounts[market_index],
                cancel_arguments[i].order_id,
                cancel_arguments[i].cancel_side
            )
        txs = utils.split_ixs_into_tx(ixs, constants.MAX_CANCELS_PER_TX)
        txIds = []
        for tx in txs:
            txIds.push(await utils.process_transaction(self._parent.provider, tx))
        return txIds
    
    async def cancel_multiple_orders_no_error(self, cancel_arguments):
        ixs = []
        for i in range(len(cancel_arguments)):
            market_index = self._sub_exchange.markets.get_market_index(
                cancel_arguments[i].market
            )
            ix = instructions.cancel_order_no_error_ix(
                self.asset,
                market_index,
                self._parent.public_key(),
                self._margin_account_address,
                self._open_orders_accounts[market_index],
                cancel_arguments[i].order_id,
                cancel_arguments[i].cancel_side
            )
            ixs.push(ix)
        txs = utils.split_ixs_into_tx(ixs, constants.MAX_CANCELS_PER_TX)
        txIds = []
        for tx in txs:
            txIds.push(await utils.process_transaction(self._parent.provider, tx))
        return txIds
    
    async def force_cancel_orders(self, market, margin_account_to_cancel):
        margin_account = await Exchange.program.account.margin_account.fetch(
            margin_account_to_cancel
        )

        market_index = self._sub_exchange.markets.get_market_index(market)

        open_orders_account_to_cancel = await utils.create_open_orders_address(
            Exchange.program_id,
            market,
            margin_account.authority,
            margin_account.open_orders_nonce[market_index]
        )

        tx = Transaction()
        ix = instructions.force_cancel_orders_ix(
            self.asset,
            market_index,
            margin_account_to_cancel,
            open_orders_account_to_cancel
        )
        tx.add(ix)
        return await utils.process_transaction(self._parent.provider, tx)
    
    async def liquidate(self, market, liquidated_margin_account, size):
        tx = Transaction()
        ix = instructions.liquidate_ix(
            self.asset,
            self._parent.public_key(),
            self._margin_account_address,
            market,
            liquidated_margin_account,
            size
        )
        tx.add(ix)
        return await utils.process_transaction(self._parent.provider, tx)
    
    async def cancel_all_orders(self):
        ixs = []
        for i in range(len(self._orders)):
            order = self._orders[i]
            ix = instructions.cancel_order_ix(
                self.asset,
                order.market_index,
                self._parent.public_key(),
                self._margin_account_address,
                self._open_orders_accounts[order.market_index],
                order.order_id,
                order.side
            )
            ixs.push(ix)
        txs = utils.split_ixs_into_txs(ixs, constants.MAX_CANCELS_PER_TX)
        txIds = []
        for tx in txs:
            txIds.push(await utils.process_transaction(self._parent.provider, tx))
        return txIds
    
    async def cancel_all_orders_no_error(self):
        ixs = []
        for i in range(len(self._orders)):
            order = self._orders[i]
            ix = instructions.cancel_order_no_error_ix(
                self.asset,
                order.market_index,
                self._parent.public_key(),
                self._margin_account_address,
                self._open_orders_accounts[order.market_index],
                order.order_id,
                order.side
            )
            ixs.push(ix)
        
        txs = utils.split_ixs_into_tx(ixs, constants.MAX_CANCELS_PER_TX)
        txIds = []
        for tx in txs:
            txIds.push(await utils.process_transaction(self._parent.provider, tx))
        return txIds
    
    async def position_movement(self, movement_type, movements):
        tx = self.get_position_movement_tx(movement_type, movements)
        return await utils.process_transaction(self._parent.provider, tx)
    
    async def simulate_position_movement(self, movement_type, movements):
        tx = self.get_position_movement_tx(movement_type, movements)
        response = await utils.simulate_transaction(self._parent.provider, tx)

        events = response.events
        position_movement_event = None

        for i in range(len(events)):
            if events[i].name == "PositionMovementEvent":
                position_movement_event = events[i].data
                break
        
        if position_movement_event == None:
            raise Exception("Failed to simulate position movement.")
        
        return position_movement_event

    def get_position_movement_tx(self, movement_type, movements):
        if len(movements) > constants.MAX_POSITION_MOVEMENTS:
            raise Exception("Max position movements exceeded. Max = " + str(constants.MAX_POSITION_MOVEMENTS) + " < " + str(len(movements)))
        
        tx = Transaction()
        self.assert_has_margin_account()
        sub_exchange = self._sub_exchange

        if self.spread_account == None:
            print("User has no spread account. Creating spread account...")
            tx.add(
                instructions.initialize_spread_account_ix(
                    sub_exchange.zeta_group_address,
                    self.spread_account_address,
                    self._parent.public_key()
                )
            )

        tx.add(
            instructions.position_movement_ix(
                sub_exchange.zeta_group_address,
                self.margin_account_address,
                self.spread_account_address,
                self._parent.public_key(),
                sub_exchange.greeks_address,
                sub_exchange.zeta_group.oracle,
                movement_type,
                movements
            )
        )

        return tx
    
    async def transfer_excess_spread_balance(self):
        tx = Transaction().add(
            instructions.transfer_excess_spread_balance_ix(
                self._sub_exchange.zeta_group_balance,
                self.margin_account_address,
                self.spread_account_address,
                self._parent.public_key()
            )
        )
        return await utils.process_transaction(self._parent.provider, tx)
    
    def get_relevant_market_indexes(self):
        indexes = []
        for i in range(len(self._margin_account.product_ledgers)):
            ledger = self._margin_account.product_ledgers[i]
            if ledger.position.size.to_number() != 0 or ledger.order_state.opening_orders[0].to_number() != 0 or ledger.order_state.opening_orders[1].to_number() != 0:
                indexes.append(i)
        return indexes
    
    async def update_orders(self):
        orders = []
        sub_exchange = self._sub_exchange
        for i in self.get_relevant_market_indexes():
            await sub_exchange.markets.markets[i].update_orderbook()
            orders.append(
                sub_exchange.markets.markets[i].get_orders_for_account(
                    self._open_orders_accounts[i]
                )
            )
        self._orders = orders

    async def update_margin_positions(self):
        positions = []
        for i in range(len(self._margin_account.product_ledgers)):
            if self._margin_account.product_ledgers[i].position.size.to_number() != 0:
                positions.append({
                    "market_index": i,
                    "market": self._sub_exchange.zeta_group.products[i].market,
                    "size": utils.convert_native_lot_size_to_decimal(
                        self._margin_account.product_ledgers[i].position.size.to_number()
                    ),
                    "cost_of_trades": utils.convert_native_lot_size_to_decimal(
                        self._margin_account.product_ledgers[i].position.cost_of_trades
                    )
                })
        self._margin_positions = positions
    
    def update_spread_positions(self):
        positions = []
        for i in range(len(self._spread_account.positions)):
            if self._spread_account.positions[i].size.to_number() != 0:
                positions.append({
                    "market_index": i,
                    "market": self._sub_exchange.zeta_group.products[i].market,
                    "size": utils.convert_native_lot_size_to_decimal(
                        self._spread_account.product_ledgers[i].position.size.to_number()
                    ),
                    "cost_of_trades": utils.convert_native_lot_size_to_decimal(
                        self._spread_account.product_ledgers[i].position.cost_of_trades
                    )
                })
        self._spread_positions = positions
    
    ### TODO: NEED TO FINISH THIS FUNCTION
    async def update_open_order_addresses(self):
        for index, product in enumerate(self._sub_exchange.zeta_group.products):
            if self._margin_account.open_orders_nonce[index] != 0 and self._open_orders_accounts[index] == PublicKey("0"):
                open_orders_pda, _open_orders_nonce = await utils.get_open_orders(
                    Exchange.program_id,
                    product.market,
                    self._parent.public_key
                )
                self._open_orders_accounts[index] = open_orders_pda

    def assert_has_margin_account(self):
        if self.margin_account == None:
            raise Exception("Margin account doesn't exist!")
    
    def get_margin_position_size(self, index, decimal):
        size = self.margin_account.product_ledgers[index].position.size.to_number()
        if decimal:
            return utils.convert_native_lot_size_to_decimal(size)
        else:
            return size
    
    def get_margin_cost_of_trades(self, index, decimal):
        cost_of_trades = self.margin_account.product_ledgers[index].position.cost_of_trades.to_number()
        if decimal:
            return utils.convert_native_integer_to_decimal(cost_of_trades)
        else:
            return cost_of_trades
        
    def get_opening_orders(self, index, side, decimal):
        order_index = None
        if side == types.Side.BID:
            order_index = 0
        else:
            order_index = 1
        
        size = self.margin_account.product_ledgers[index].order_state.opening_orders[order_index].to_number()
        if decimal:
            return utils.convert_native_lot_size_to_decimal(size)
        else:
            return size
    
    def get_closing_orders(self, index, decimal):
        size = self.margin_account.product_ledgers[index].order_state.closing_orders.to_numbers()
        if decimal:
            return utils.convert_native_lot_size_to_decimal(size)
        else:
            return size
    
    def get_spread_position_size(self, index, decimal):
        size = self.spread_account.positions[index].size.to_number()
        if decimal:
            return utils.convert_native_lot_size_to_decimal(size)
        else:
            return size
        
    def get_spread_cost_of_trades(self, index, decimal):
        cost_of_trades = self.spread_account.positions[index].cost_of_trades.to_number()
        if decimal:
            return utils.convert_native_integer_to_decimal(cost_of_trades)
        return cost_of_trades
    
    
    
    async def close(self):
        if self._margin_account_subscription_id != None:
            await self._parent.provider.connection.remove_account_change_listener(
                self._margin_account_subscription_id
            )
            self._margin_account_subscription_id = None
        
        if self._spread_account_subscription_id != None:
            await self._parent.provider.connection.remove_account_change_listener(
                self._spread_account_subscription_id
            )
            self._spread_account_subscription_id = None
        
        if self._trade_event_listener != None:
            await Exchange.program.remove_event_listener(self._trade_event_listener)
            self._trade_event_listener = None