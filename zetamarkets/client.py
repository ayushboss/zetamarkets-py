from program_instructions import initialize_margin_account_tx, deposit_ix
from anchorpy.utils import get_token_account_info
from solana.publickey import PublicKey
from solana.transaction import Transaction
from anchorpy import Program, Provider, Wallet
from exchange import Exchange

class Client:
    def public_key(self):
        return self._provider.wallet.public_key

    @property
    def provider(self):
        return self._provider

    @property
    def margin_account(self):
        return self._margin_account

    @property
    def margin_account_address(self):
        return self._margin_account_address

    @property
    def spread_account(self):
        return self._spread_account

    @property
    def spread_account_address(self):
        return self._spread_account_address

    @property
    def usdc_account_address(self):
        return self._usdc_account_address

    @property
    def open_orders_accounts(self):
        return self._open_orders_accounts

    @property
    def orders(self):
        return self._orders

    @property
    def positions(self):
        return self._positions

    @property
    def spread_positions(self):
        return self._spread_positions

    @property
    def whitelist_deposit_address(self):
        return self._whitelist_deposit_address

    @property
    def whitelist_trading_fees_address(self):
        return self._whitelist_trading_fees_address


    def __init__(self, connection, wallet, opts):
        self._provider = Provider(connection, wallet, opts)
        self._program = Program(idl, Exchange.program_id, self._provider)

        self._open_orders_accounts = [PublicKey.default] * len(Exchange.zetaGroup.products)

        self._positions = []
        self._orders = []
        self._last_update_timestamp = 0
        self._pedning_update = False
        self._margin_account = None
        self._spread_account = None

    def deposit(self, amount: float):
        self._usdc_account_check()
        tx = Transaction()
        if self._margin_account is not None:
            print("User has no margin account. Creating margin account...")
            tx = initialize_margin_account_tx(self.public_key)
            tx.add(initialize_margin_account_ix(exchange.zeta_group_address, self._margin_account_address, self.public_key))
        tx.add(
            await instructions.deposit_ix(amount, self._margin_account_address, self._usdc_account_address, self.public_key, self._whitelist_deposit_address)
        )
        tx_id = await utils.process_transaction(self._provider, tx)
        # Add deposit transaction
        pass

    @staticmethod
    async def load(connection, wallet, opts, callback, throttle):
        print(f"Loading client: {wallet.public_key}")
        client = Client(connection, wallet, opts)
        [margin_account_address, _margin_account_nonce] = await utils.get_margin_account(Exchange.program_id, Exchange.zeta_group_address, wallet.public_key)
        [spread_account_address, _spread_account_nonce] = await utils.get_spread_account(Exchange.program_id, Exchange.zeta_group_address, wallet.public_key)
        client._margin_account_address = margin_account_address
        client._spread_account_address = spread_account_address
        pass

    def _usdc_account_check(self):
        try:
            token_account_info = get_token_account_info(
                self._provider, self._usdc_token_account
            )
            print(
                f"Found user USDC associated token_acount {self._usdc_account_address}. Balance= ${token_account_info.amount}"
            )
        except:
            raise (
                "User has no USDC associated token account. Please create one and deposit USDC."
            )
    def place_order(market, price, size, side, client_order_id=0):
        tx = Transaction()
        market_index = Exchange._markets.get_market_index(market)
        open_orders_pda = None
        pass
