from exchange import Exchange
from solana.publickey import PublicKey
import constants
import utils

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
    
    def __init__(self, asset, parent):
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
        self._spread_account = None
        self._poll_interval = constants.DEFAULT_CLIENT_POLL_INTERVAL
        self._updating_state = False
        self._updating_state_timestamp = None
    
    async def load(self, asset, parent, connection, wallet, callback = None, throttle = False):
        subClient = SubClient(asset, parent)
        margin_account_address, _margin_account_nonce = await utils.get_margin_account(
            Exchange.program_id,
            subClient._sub_exchange.zeta_group_address,
            wallet.publicKey
        )

        spread_account_address, _spread_account_nonce = await utils.get_spread_account(
            Exchange.program_id,
            subClient._sub_exchange.zeta_group_address,
            wallet.publicKey
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
        
