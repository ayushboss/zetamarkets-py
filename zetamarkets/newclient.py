from sqlite3 import SQLITE_DROP_TEMP_INDEX
import program_instructions as instructions
from program_instructions import initialize_margin_account_tx, deposit_ix
from anchorpy.utils import get_token_account_info
from solana.transaction import Transaction
from anchorpy import Program, Provider, Wallet
import utils
from exchange import Exchange
import constants
from newsubclient import SubClient

class Client:
    def public_key(self):
        return self._provider.wallet.public_key

    @property
    def provider(self):
        return self._provider
    
    @property
    def connection(self):
        return self._provider.connection
    
    @property
    def referral_account(self):
        return self._referral_account
    
    def referral_account_address(self):
        return self._referral_account_address

    @property
    def referrer_account(self):
        return self._referrer_account
    
    @property
    def referrer_alias(self):
        return self._referrer_alias
    
    @property
    def usdc_account_address(self):
        return self._usdc_account_address
    
    @property
    def whitelist_deposit_address(self):
        return self._whitelist_deposit_address
    
    @property
    def whitelist_trading_fees_address(self):
        return self._whitelist_trading_fees_address

    @property
    def subclients(self):
        return self._subclients

    def __init__(self, connection, wallet: Wallet, opts):
        self._provider = Provider(connection, wallet, opts)
        self._subclients = {}
        self._referral_account = None
        self._referrer_account = None
        self._referrer_account = None
        self._whitelist_deposit_address = None
        self._whitelist_trading_fees_address = None
        self._usdc_account_address = None
        self._referral_alias = None
    
    async def load(connection, wallet: Wallet, opts, callback, throttle):
        client = Client(connection, wallet, opts)
        client._usdc_account_address = await utils.get_associated_token_address(
            Exchange._usdc_mint_address,
            wallet.public_key
        )

        client._whitelist_deposit_address = None
        try:
            whitelist_deposit_address, _whitelist_trading_fees_nonce = await utils.get_user_whitelist_deposit_account(
                Exchange.program_id,
                wallet.public_key
            )
            ### TODO: REFACTOR THESE LINES
            await Exchange.program.account.whitelist_deposit_account.fetch(
                whitelist_deposit_address
            )
            print("User is whitelisted for unlimited deposits into zeta.")
            client._whitelist_deposit_address = whitelist_deposit_address
        except:
            print("An error occured during the whitelisting process")
        
        client._whitelist_trading_fees_address = None
        try:
            whitelist_trading_fees_address, _whitelist_trading_fees_nonce = await utils.get_user_whitelist_trading_fees_account(
                Exchange.program_id,
                wallet.public_key
            )
            await Exchange.program.account.whitelist_trading_fees_account.fetch(
                whitelist_trading_fees_address
            )
            print("User is whitelisted for trading fees")
            client._whitelist_trading_fees_address = whitelist_trading_fees_address
        except:
            print("An error occurred during the whitelisting trading fees process")
        
        for asset in Exchange._assets:
            subclient = await SubClient.load(
                asset,
                client,
                connection,
                wallet,
                callback,
                throttle
            )
            client.add_sub_client(asset, subclient)
        
        client.set_polling(constants.DEFAULT_CLIENT_TIMER_INTERVAL)
        client._referral_account_address = None
        client._referral_alias = None
        
        return client
    
    def add_sub_client(self, asset, subclient):
        self._subclients[asset] = subclient
    
    def get_sub_client(self, asset) -> SubClient:
        return self._subclients[asset]
    
    def get_all_subclients(self) -> list[SubClient]:
        self._subclients.values()
    
    async def set_referral_data(self):
        try:
            referrerAccount = utils.get_referrer_account_address(
                Exchange.program_id,
                self.public_key()
            )
            self._referrer_account = (await Exchange.program.account.referrerAccount.fetch(
                referrerAccount
            ))
            print("User is a referrer. " + self.public_key())

            referrer_alias = await utils.fetch_referrer_alias_account(self.public_key())
            if referrer_alias != None:
                existing_alias = referrer_alias.alias
                self._referrer_alias = existing_alias
        except:
            print("An error occurred while forming the referrer accounts")
        
        try:
            referral_account_address_loc, _nonce = await utils.get_referral_account_address(
                Exchange.program_id,
                self.public_key()
            )

            self._referral_account_address = referral_account_address_loc
            self._referral_account = await Exchange.program.account.referralAccount.fetch(
                referral_account_address_loc
            )

            print("User has been referred by " + str(self._referral_account))
        except:
            print("An error occurred while forming the referral accounts")
    
    async def refer_user(self, referrer):
        referrer_account = await utils.get_referrer_account_address(
            Exchange.program_id,
            referrer
        )

        try:
            await Exchange.program.account.referrerAccount.fetch(referrer_account)
        except:
            print("Error when trying to pull the referrer account")
        
        tx = Transaction().add(
            await instructions.refer_user_ix(self.provider.wallet.public_key, referrer)
        )
        txId = await utils.process_transaction(self.provider, tx)

        self._referral_account = await Exchange.program.account.referralAccount.fetch(
            self._referral_account_address
        )
        return txId
    
    def set_polling(self, timer_interval):
        if self._poll_interval_id != None:
            print("Resetting existing timer to " + str(timer_interval) + " seconds")
            clear_interval(self._poll_interval_id)
        
        ### TODO: NEED SOME SORT OF SET INTERVAL THING EQUIVALENT
    def market_identifier_to_public_key(asset, market):
        market_pubkey = None
        if isinstance(market, int):
            market_pubkey = Exchange.get_sub_exchange(asset).markets.markets[market].address
        else:
            market_pubkey = market
        return market_pubkey
    
    async def place_order(self, asset, market, price, size, side, type, client_order_id, tag):
        ret = await self.get_sub_client(asset).place_order_v3(
            self.market_identifier_to_public_key(asset, market),
            price,
            size,
            side,
            type,
            client_order_id,
            tag
        )
        return ret
    
    async def migrate_funds(self, amount, withdraw_asset, deposit_asset):
        tx = Transaction()
        withdraw_sub_client = self.get_sub_client(withdraw_asset)
        deposit_sub_client = self.get_sub_client(deposit_asset)

        tx.add(
            instructions.withdraw_ix(
                withdraw_asset,
                amount,
                withdraw_sub_client.margin_account_address,
                self.usdc_account_address,
                self.public_key()
            )
        )

        if deposit_sub_client.margin_account == None:
            print("User has no margin account. Creating margin account...")
            tx.add(
                instructions.initialize_margin_account_ix(
                    deposit_sub_client.sub_exchange.zeta_group_address,
                    deposit_sub_client.margin_account_address,
                    self.public_key()
                )
            )
        tx.add(
            await instructions.deposit_ix(
                deposit_asset,
                amount,
                deposit_sub_client.margin_account_address,
                self.usdc_account_address,
                self.public_key(),
                self.whitelist_deposit_address
            )
        )

        return await utils.process_transaction(self.provider, tx)

    async def deposit(self, asset, amount):
        await self.usdc_account_check()
        return await self.get_sub_client(asset).deposit(amount)

    async def usdc_account_check(self):
        try:
            token_account_info = await utils.get_token_account_info(
                self.provider.connection,
                self.usdc_account_address
            )
            print("Found user USDC associated token account " + str(self.usdc_account_address) + ", Balance = " + str(utils.convert_native_lot_size_to_decimal(token_account_info.amount)))
        except:
            raise Exception("User has no USDC associated token account. Please create one and deposit USDC.")
    
    async def update_state(self, asset, fetch = True, force = False):
        if asset:
            await self.get_sub_client(asset).update_state(fetch, force)
        else:
            for subclient in self.get_all_subclients():
                await subclient.update_state(fetch, force)
    
    async def cancel_all_orders(self, asset = None):
        if asset:
            return await self.get_sub_client(asset).cancel_all_orders()
        else:
            allTxIds = []
            for subclient in self.get_all_subclients():
                txids = await subclient.cancel_all_orders()
                allTxIds.append(txids)
            return allTxIds
    
    async def cancel_all_orders_no_error(self, asset = None):
        if asset:
            return await self.get_sub_client(asset).cancel_all_orders_no_error()
        else:
            allTxIds = []
            for subclient in self.get_all_subclients():
                txids = await subclient.cancel_all_orders_no_error()
                allTxIds.append(txids)
            return allTxIds
    
    def get_margin_account_state(self, asset):
        return Exchange.risk_calculator.get_margin_account_state(self.get_sub_client(asset).margin_account)
    
    async def close_margin_account(self, asset):
        return await self.get_sub_client(asset).close_margin_account()
    
    async def close_spread_account(self, asset):
        return await self.get_sub_client(asset).close_spread_account()
    
    async def withdraw(self, asset, amount):
        return await self.get_sub_client(asset).withdraw(amount)
    
    async def withdraw_and_close_margin_account(self, asset):
        return await self.get_sub_client(asset).withdraw_and_close_margin_account()
    
    async def place_order_and_lock_position(self, asset, market, price, size, side, tag = "SDK"):
        return await self.get_sub_client(asset).place_order_and_lock_position(
            self.market_identifier_to_public_key(asset, market),
            price,
            size,
            side,
            tag
        )
    
    async def cancel_order(self, asset, market, order_id, side):
        market_pubkey = self.market_identifier_to_public_key(asset, market)
        return await self.get_sub_client(asset).cancel_order(
            market_pubkey,
            order_id,
            side
        )

    async def cancel_order_by_client_order_id(self, asset, market, client_order_id):
        market_pubkey = self.market_identifier_to_public_key(asset, market)
        return await self.get_sub_client(asset).cancel_order_by_client_order_id(
            market_pubkey,
            client_order_id
        )

    async def cancel_and_place_order(self, asset, market, order_id, cancel_side, new_order_price, new_order_size, new_order_side, new_order_type, client_order_id, new_order_tag):
        return await self.get_sub_client(asset).cancel_and_place_order_v3(
            self.market_identifier_to_public_key(asset, market),
            order_id,
            cancel_side,
            new_order_price,
            new_order_size,
            new_order_side,
            new_order_type,
            client_order_id,
            new_order_tag
        )

    async def cancel_and_place_order_by_client_order_id(self, asset, market, cancel_client_order_id, new_order_price, new_order_size, new_order_side, new_order_type, new_order_client_order_id, new_order_tag):
        return await self.get_sub_client(asset).cancel_and_place_order_by_client_order_id_v3(
            self.market_identifier_to_public_key(asset, market),
            cancel_client_order_id,
            new_order_price,
            new_order_size,
            new_order_side,
            new_order_type,
            new_order_client_order_id,
            new_order_tag
        )

    async def replace_by_client_order_id(self, asset, market, cancel_client_order_id, new_order_price, new_order_size, new_order_side, new_order_type, new_order_client_order_id, new_order_tag):
        return await self.get_sub_client(asset).replace_by_client_order_id_v3(
            self.market_identifier_to_public_key(asset, market),
            cancel_client_order_id,
            new_order_price,
            new_order_size,
            new_order_side,
            new_order_type,
            new_order_client_order_id,
            new_order_tag
        )
    
    async def initialize_open_orders_account(self, asset, market):
        return await self.get_sub_client(asset).initialize_open_orders_account(market)
    
    async def close_open_orders_account(self, asset, market):
        return await self.get_sub_client(asset).close_open_orders_account(market)
    
    async def close_multiple_open_orders_account(self, asset, markets):
        return await self.get_sub_client(asset).close_multiple_open_orders_account(markets)
    
    async def cancel_multiple_orders(self, asset, cancel_arguments):
        return await self.get_sub_client(asset).cancel_multiple_orders(cancel_arguments)
    
    async def cancel_multiple_orders_no_error(self, asset, cancel_arguments):
        return await self.get_sub_client(asset).cancel_multiple_orders_no_error(cancel_arguments)
    
    async def force_cancel_orders(self, asset, market, margin_account_to_cancel):
        return await self.get_sub_client(asset).force_cancel_orders(
            self.market_identifier_to_public_key(asset, market),
            margin_account_to_cancel
        )

    async def liquidate(self, asset, market, liquidated_margin_account, size):
        return await self.get_sub_client(asset).liquidate(
            self.market_identifier_to_public_key(asset, market),
            liquidated_margin_account,
            size
        )
    
    async def position_movement(self, asset, movement_type, movements):
        return await self.get_sub_client(asset).position_movement(
            movement_type,
            movements
        )
    
    async def simulate_position_movement(self, asset, movement_type, movements):
        return await self.get_sub_client(asset).simulate_position_movement(
            movement_type,
            movements
        )

    async def transfer_excess_spread_balance(self, asset):
        return await self.get_sub_client(asset).transfer_excess_spread_balance()
    
    def get_margin_position_size(self, asset, index, decimal = False):
        return self.get_sub_client(asset).get_margin_position_size(index, decimal)
    
    def get_margin_cost_of_trades(self, asset, index, decimal):
        return self.get_sub_client(asset).get_margin_cost_of_trades(index, decimal)
    
    def get_margin_positions(self, asset):
        return self.get_sub_client(asset).margin_positions
    
    def get_spread_positions(self, asset):
        return self.get_sub_client(asset).spread_positions
    
    def get_orders(self, asset):
        return self.get_sub_client(asset).orders
    
    def get_opening_orders(self, asset, index, side, decimal):
        return self.get_sub_client(asset).get_opening_orders(index, side, decimal)
    
    def get_closing_orders(self, asset, index, decimal):
        return self.get_sub_client(asset).get_closing_orders(index, decimal)
    
    def get_open_orders_accounts(self, asset):
        return self.get_sub_client(asset).open_orders_accounts
    
    def get_spread_position_size(self, asset, index, decimal):
        return self.get_sub_client(asset).get_spread_position_size(index, decimal)
    
    def get_spread_cost_of_trades(self, asset, index, decimal):
        return self.get_sub_client(asset).get_spread_cost_of_trades(index, decimal)
    
    def get_spread_account(self, asset):
        return self.get_sub_client(asset).spread_account
    
    def get_spread_account_address(self, asset):
        return self.get_sub_client(asset).spread_account_address
    
    def get_margin_account(self, asset):
        return self.get_sub_client(asset).margin_account
    
    def get_margin_account_address(self, asset):
        return self.get_sub_client(asset).margin_account_address
    
    async def initialize_referrer_alias(self, alias):
        if len(alias) > 15:
            raise Exception("Alias cannot be over 15 chars!")
        
        referrer_account_address = await utils.get_referrer_account_address(
            Exchange.program_id,
            self.public_key()
        )

        referrer_alias_address = await utils.get_referrer_alias_address(
            Exchange.program_id,
            alias
        )

        referrer_account = None
        try:
            referrer_account = await Exchange.program.account.referrerAccount.fetch(
                referrer_account_address
            )
        except:
            raise Exception("User is not a referrer, cannot create alias.")
        
        referrer_alias = await utils.fetch_referrer_alias_account(self.public_key())
        if referrer_alias != None:
            # existing_alias = str(Buffer.from(referrer_alias))
            raise Exception("Referrer already has alias.")
        
        tx = Transaction().add(
            await instructions.initialize_referrer_alias_ix(self.public_key(), alias)
        )

        txid = await utils.process_transaction(self.provider, tx)
        self._referrer_alias = alias

        return txid
    
    async def close(self):
        for subclient in self.get_all_subclients():
            subclient.close()
        # if self._pollIntervalId != None:
        #     clear_int
        
        ## FIGURE OUT INTERVAL AND CLEARING INTERVAL IN PYTHON
