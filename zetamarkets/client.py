from program_instructions import initialize_margin_account_tx
from anchorpy.utils import get_token_account_info
from solana.transaction import Transaction


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


    def __init__(self, connection, wallet, opts):
        pass

    def deposit(self, amount: float):
        # self.usd
        self._usdc_account_check()
        tx = Transaction()
        if self._margin_account is not None:
            print("User has no margin account. Creating margin account...")
            tx = initialize_margin_account_tx(self.public_key)
        # Add deposit transaction
        pass

    @staticmethod
    async def load(connection, wallet, opts, callback, throttle):
        # get margin, spread, usdc, and then whitelist
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
