import json
from zetamarkets.constants import IDL_PATH, CLUSTER_URLS
import constants
from zetamarkets.oracle import Oracle
# from zetamarkets.risk import RiskCalculator
from zetamarkets import utils,events
from typing import Callable
from anchorpy import Provider, Idl, Program
from solana.publickey import PublicKey
from solana.transaction import Transaction

class ExchangeMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Exchange(metaclass=ExchangeMeta):
    _mint_authority = None
    _state = None
    _serum_authority = None
    _instance = None
    program_id = None
    is_initialized = False
    _is_setup = True
    
    @property
    def oracle(self):
        return self._oracle

    @property
    def zetagroup(self):
        return self._zetagroup

    @property
    def state_address(self):
        return self._state_address

    @property
    def greeks(self):
        return self._greeks
    
    @property
    def use_ledger(self):
        return self._use_ledger
    
    _use_ledger = False

    def set_ledger_wallet(self, wallet):
        self._use_ledger = True
        self._ledger_wallet = wallet

    def __init__(self, program_id, network, connection, wallet):
        # TODO: Come back to this later and see if relevant
        pass

    async def _init(self, program_id, network, connection, wallet, opts, assets):
        self._provider = Provider(connection, wallet, opts)
        self._network = network
        self._oracle = Oracle(self._network, connection)
        self._connection = connection
        with IDL_PATH.open() as f:
            raw_idl = json.load(f)
        idl = Idl.from_json(raw_idl)
        self._program = Program(idl, program_id, self._provider)
        # self._risk_calculator = RiskCalculator()
        self._program_id = program_id
        self._last_poll_timestamp = 0
        self._zetagroup = None
        self._state_address = None
        self._is_initialized = False
        self._assets = assets
        self._opts = opts
        for asset in assets:
            await self.add_sub_exchange(asset, SubExchange())
            await self.get_sub_exchange(asset).initialize(asset)
        self._is_setup = True

    async def initialize_zeta_state(self, params):
        mint_authority, mint_authority_nonce = await utils.get_mint_authority(
            self._program_id
        )
        state, state_nonce = await utils.get_state(self._program_id)
        serum_authority, serum_nonce = await utils.get_serum_authority(
            self._program_id
        )

        self._usdc_mint_address = constants.USDC_MINT_ADDRESS[self._network]

        treasury_wallet, _treasury_wallet_nonce = await utils.get_zeta_treasury_wallet(self._program_id, self._usdc_mint_address)

        tx = Transaction().add(
            instructions.initialize_zeta_state_ix(
                state,
                state_nonce,
                serum_authority,
                treasury_wallet,
                serum_nonce,
                mint_authority,
                mint_authority_nonce,
                params
            )
        )
        try:
            await utils.process_transaction(self._provider, tx)
        except:
            print("Initialize zeta state failed")
        
        self._mint_authority = mint_authority
        self._state_address = state
        self._serum_authority = serum_authority
        self._treasury_wallet_address = treasury_wallet
        await self.update_state()

    async def initialize_zeta_group(self, asset, oracle, pricing_args, margin_args):
        tx = Transaction().add(
            await instructions.initialize_zeta_group_ix(
                asset,
                constants.MINTS[asset],
                oracle,
                pricing_args,
                margin_args
            )
        )

        try:
            await utils.process_transaction(
                self._provider,
                tx,
                [],
                utils.default_commitment(),
                self.use_ledger
            )
        except:
            print("Initialize zeta group failed")

        await self.update_state()
        await self.get_sub_exchange(asset).update_zeta_group()

    @classmethod
    async def load(self, cls, program_id: PublicKey, network, connection, opts, wallet, throttle_ms, assets, callback):
        if self.is_initialized:
            raise Exception("Exchange already loaded")
        if not self._is_setup:
            await self._init(
                self,
                program_id,
                network,
                connection,
                wallet,
                opts,
                assets
            )
        self._risk_calculator = RiskCalculator(self.assets)
        self._connection = connection
        mint_authority, _mint_authority_nonce = await utils.get_mint_authority(
            self.program_id
        )
        state, _state_nonce = await utils.get_state(self.program_id)
        serum_authority, _serum_nonce = await utils.get_serum_authority(
            self.program_id
        )

        self._mint_authority = mint_authority
        self._state_address = state
        self._serum_authority = serum_authority
        self._usdc_mint_address = constants.USDC_MINT_ADDRESS[network]

        treasury_wallet, _treasury_wallet_nonce = await utils.get_zeta_treasury_wallet(self.program_id, self._usdc_mint_address)
        self._treasury_wallet_address = treasury_wallet

        self._last_poll_timestamp = 0

        self._oracle = Oracle(network, connection)
        await self.subscribe_oracle(self.assets, callback)

        for asset in assets:
            await self.get_sub_exchange(asset).load(
                asset,
                self.program_id,
                self.network,
                self.opts,
                throttle_ms,
                callback
            )
        
        for asset in assets:
            gt = self.get_markets(asset)
            for each in gt:
                self._markets.append(each)
        
        await self.update_state()
        await self.subscribe_clock(callback)

        self._is_initialized = True
    
    async def add_sub_exchyange(self, asset, sub_exchange):
        self._sub_exchanges[asset] = sub_exchange
    
    def get_sub_exchange(self, asset):
        try:
            return self._sub_exchanges[asset]
        except:
            raise Exception("Failed to get subexchange for asset, have you called Exchange.load()?")
        
    def get_all_sub_exchanges(self):
        return self._sub_exchanges.values()
    
    def subscribe_inline_callback(self, asset, price, callback):
        if self._is_initialized:
            self._risk_calculator.update_margin_requirements(asset)
        if callback != None:
            callback(asset, EventType.Oracle, price)

    async def subscribe_oracle(self, assets, callback1):
        await self._oracle.subscribe_price_feeds(
            assets,
            callback1,
        )
    
    def set_clock_data(self, data):
        self._clock_timestamp = data

    ### TODO: NEED TO FIGURE OUT CLOCK THINGS

    # async def subscribe_clock(self, callback):
    #     if self._clock_subscription_id != None:
    #         raise Exception("Clock already subscribed to")
        
    #     self._clock_subscription_id = self._provider.connection.on_account_change(
    #         constants.
    #     )

    def add_program_subscription_id(self, id):
        self._program_subscription_ids.push(id)
    
    async def update_exchange_state(self):
        await self.update_state()
        for asset in self._assets:
            await self.update_zeta_group(asset)
            self.get_zeta_group_markets(asset).update_expiry_series()
    
    async def update_state(self):
        self._state = await self._program.account.state.fetch(
            self.state_address
        )
    
    async def update_zeta_state(self, params):
        tx = Transaction().add(
            instructions.update_zeta_state_ix(params, self._provider.wallet.publicKey)
        )
        await utils.process_transaction(self._provider, tx)
        await self.update_state()
    
    async def initialize_market_nodes(self, asset, zeta_group):
        await self.get_sub_exchange(asset).initialize_market_nodes(zeta_group)
    
    def subscribe_market(self, asset, index):
        self.get_sub_exchange(asset).markets.subscribe_market(index)
    
    def unsubscribe_market(self, asset, index):
        self.get_sub_exchange(asset).markets.unsubscribe_market(index)
    
    async def update_orderbook(self, asset, index):
        await self.get_sub_exchange(asset).markets.markets[index].update_orderbook()
    
    async def update_all_orderbooks(self, live):
        all_live_markets = self._markets
        if live:
            all_live_markets = []
            for m in self._markets:
                if m.expiry_series.is_live():
                    all_live_markets.push(m)
        
        live_markets_slices = []
        i = 0
        while i < len(all_live_markets):
            live_markets_slices.push(
                all_live_markets[i:i+constants.MAX_MARKETS_TO_FETCH]
            )
            i+=constants.MAX_MARKETS_TO_FETCH
        
        for live_markets in live_markets_slices:
            live_market_ask_addresses = []
            for m in live_markets:
                live_market_ask_addresses.push(m.serum_market.asks_address)
            
            live_market_bid_addresses = []
            for m in live_markets:
                live_market_bid_addresses.push(m.serum_market.bids_address)

            comb = live_market_ask_addresses
            for each in live_market_bid_addresses:
                comb.append(each)

            account_infos = await self._connection.get_multiple_accounts_info(
                comb
            )

            half = (len(account_infos)/2)+1
            asks_account_infos = account_infos[0:half]
            bids_account_infos = account_infos[half+1:]

            live_markets_to_ask_account_infos_map = {}
            live_markets_to_bid_account_infos_map = {}

            for m, i in enumerate(live_markets):
                live_markets_to_ask_account_infos_map[m] = asks_account_infos[i]
                live_markets_to_bid_account_infos_map[m] = bids_account_infos[i]
            
            for market in live_markets:
                market.asks = Orderbook.decode(
                    market.serum_market,
                    live_markets_to_ask_account_infos_map[market].data
                )
                market.bids = Orderbook.decode(
                    market.serum_market,
                    live_markets_to_bid_account_infos_map[market].data
                )
                market.update_orderbook(False)

    def get_zeta_group_markets(self, asset):
        return self.get_sub_exchange(asset).markets
    
    def get_market(self, asset, index):
        return self.get_sub_exchange(asset).markets.markets[index]
    
    def get_markets(self, asset):
        return self.get_sub_exchange(asset).markets.markets
    
    def get_markets_by_expiry_index(self, asset, index):
        return self.get_sub_exchange(asset).markets.get_markets_by_expiry_index(index)
    
    def get_expiry_series_list(self, asset):
        return self.get_sub_exchange(asset).markets.expiry_series
    
    def get_zeta_group(self, asset):
        return self.get_sub_exchange(asset).zeta_group
    
    def get_zeta_group_address(self, asset):
        return self.get_sub_exchange(asset).zeta_group_address
    
    def get_greeks(self, asset):
        return self.get_sub_exchange(asset).greeks
    
    def get_orderbook(self, asset, index):
        return self.get_sub_exchange(asset).markets.markets[index].orderbook
    
    def get_mark_price(self, asset, index: int) -> int:
        return self.get_sub_exchange(asset).get_mark_price(index)
    
    def get_insurance_vault_address(self, asset):
        return self.get_sub_exchange(asset).insurance_vault_address

    def get_vault_address(self, asset):
        return self.get_sub_exchange(asset).vault_address
    
    def get_socialized_loss_account_address(self, asset):
        return self.get_sub_exchange(asset).socialized_loss_account_address
    
    async def update_pricing_parameters(self, asset, args):
        await self.get_sub_exchange(asset).update_pricing_parameters(args)
    
    def get_margin_params(self, asset):
        return self.get_sub_exchange(asset).margin_params
    
    async def update_margin_parameters(self, asset, args):
        await self.get_sub_exchange(asset).update_margin_parameters(args)
    
    async def update_volatility_nodes(self, asset, nodes):
        await self.get_sub_exchange(asset).update_volatility_nodes(nodes)
    
    async def initialize_zeta_markets(self, asset):
        await self.get_sub_exchange(asset).initialize_zeta_markets()
    
    async def initialize_market_strikes(self, asset):
        await self.get_sub_exchange(asset).initialize_market_strikes()
    
    async def update_zeta_group(self, asset):
        await self.get_sub_exchange(asset).update_zeta_group()
    
    async def update_pricing(self, asset, expiry_index):
        await self.get_sub_exchange(asset).update_pricing(expiry_index)
    
    async def retreat_market_nodes(self, asset, expiry_index):
        await self.get_sub_exchange(asset).retreat_market_nodes(expiry_index)
    
    async def update_sub_exchange_state(self, asset):
        await self.get_sub_exchange(asset).update_sub_exchange_state()
    
    async def whitelist_user_for_deposit(self, asset, user):
        await self.get_sub_exchange(asset).whitelist_user_for_deposit(user)
    
    async def whitelist_user_for_insurance_vault(self, asset, user):
        await self.get_sub_exchange(asset).whitelist_user_for_insurance_vault(user)
    
    async def whitelist_user_for_trading_fees(self, asset, user):
        await self.get_sub_exchange(asset).whitelist_user_for_trading_fees(user)
    
    async def treasury_movement(self, asset, treasury_movement_type, amount):
        await self.get_sub_exchange(asset).treasury_movement(
            treasury_movement_type,
            amount
        )



    async def _subscribe_oracle(self, assets, callback: Callable):
        def _subscribe_oracle_helper(asset, price):
            if self._is_initialized:
                # TODO: Patch after writing margin calculator
                print("Update margin requirements")
            if callback is not None:
                callback(events.EventType.ORACLE, price)

        await self._oracle.subscribe_price_feeds()

    def initialize_zetamarkets(self):
        # TODO: Add logic
        self._is_initialized = True

    async def update_state(self):
        """
        Polls the on chain account to update state

        """
        self.state = await self._program.account.get('State').fetch(self.state_address)

    async def update_zeta_group(self):
        self._zeta_group = await self._program.account.get('ZetaGroup').fetch(self._zeta_group_address)
        self.update_margin_params()

    def update_margin_params(self):
        if self._zeta_group is None:
            return
        self._margin_params = {
            "futureMarginInitial": self._zeta_group.margin_parameters.future_margin_initial,
            "futureMarginMaintenance":  self._zeta_group.margin_parameters.future_margin_maintenance,
            "optionMarkPercentageLongInitial": self._zeta_group.margin_parameters.option_mark_percentage_long_initial,
            "optionSpotPercentageLongInitial": self._zeta_group.margin_parameters.option_spot_percentage_long_initial,
            "optionSpotPercentageShortInitial": self._zeta_group.margin_parameters.option_spot_percentage_short_initial,
            "optionDynamicPercentageShortInitial": self._zeta_group.margin_parameters.option_dynamic_percentage_short_initial,
            "optionMarkPercentageLongMaintenance": self._zeta_group.margin_parameters.option_spot_percentage_short_maintenance,
            "optionSpotPercentageLongMaintenance": self._zeta_group.margin_parameters.option_spot_percentage_long_maintenance,
            "optionSpotPercentageShortMaintenance": self._zeta_group.margin_parameters.option_spot_percentage_short_maintenance,
            "optionDynamicPercentageShortMaintenance": self._zeta_group.margin_parameters.option_dynamic_percentage_short_maintenance,
            "optionShortPutCapPercentage": self._zeta_group.margin_parameters.option_short_put_cap_percentage
        }

