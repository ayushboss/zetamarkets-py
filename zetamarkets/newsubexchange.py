from assets import Asset
from solana.publickey import PublicKey
from exchange import Exchange
import constants
import utils
from zetamarkets.assets import assetToName
from zetamarkets.network import Network
import my_client.accounts

class SubExchange:

    @property
    def zeta_group(self):
        return self._zeta_group

    def _init_(self):
        self._is_setup = False
        self._is_initialized = False
        self._zeta_group = None ### need to implement the zetagroup class
        self._asset = Asset.UNDEFINED
        self._zeta_group_address = PublicKey("0")
        self._vault_address = PublicKey("0")
        self._insurance_vault_address = PublicKey("0")
        self._socialized_loss_account_address = PublicKey("0")
        self._markets = None ### need to implement the zeta group markets class
        self._event_emitters = []
        self._greeks = None ### need to implement greeks class
        self._greeks_address = PublicKey("0")
        self._margin_params = None ### need to implement whatever this is

    async def initialize(self, asset: Asset):
        if self._is_setup:
            raise Exception("SubExchange already initialized")
        
        self._asset = asset

        underlying_mint = constants.MINTS[asset]
        zeta_group, _zeta_group_nonce = await utils.get_zeta_group(
            Exchange.program_id,
            underlying_mint
        )
        self._zeta_group_address = zeta_group

        greeks, _greeks_nonce = await utils.get_greeks(
            Exchange.program_id,
            self._zeta_group_address
        )

        self._greeks_address = greeks

        vault_address, _vault_nonce = await utils.get_vault(
            Exchange.program_id,
            self._zeta_group_address
        )

        insurance_vault_address, _insurance_nonce = await utils.get_zeta_insurance_vault(
            Exchange.program_id,
            self._zeta_group_address
        )

        socialized_loss_account, _socialized_loss_account_nonce = await utils.get_socialized_loss_account(
            Exchange.program_id,
            self._zeta_group_address
        )

        self._vault_address = vault_address
        self._insurance_vault_address = insurance_vault_address
        self._socialized_loss_account_address = socialized_loss_account

        self._is_setup = True
    
    async def load(self, asset: Asset, program_id: PublicKey, network: Network, opts, throttle_ms = 0, callback):
        print("Loading " + assetToName(asset) + " subexchange")
        if self._is_initialized:
            raise Exception("SubExchange already loaded.")
        
        await self.update_zeta_group()

        self._markets = await ZetaGroupMarkets.load(self.asset, opts, 0)

        if self._zeta_group.products[self._zeta_group.products.length - 1].market == PublicKey("0"):
            raise Exception("Zeta group markets are uninitialized!")
        
        self._markets = await ZetaGroupMarkets.load(asset, opts, throttle_ms)
        self._greeks = (await my_client.accounts.greeks.Greeks.fetch(
            Exchange._connection,
            self._greeks_address,
            utils.default_commitment()
        ))

        Exchange.risk_calculator.update_margin_requirements(asset)

        self.subscribe_zeta_group(asset, callback)
        self.subscribe_greeks(asset, callback)

        self._is_initialized = True

        print(str(assetToName(asset)) + " subexchange loaded!")
    
    async def update_zeta_group(self):
        self._zeta_group = await my_client.accounts.zeta_group.ZetaGroup.fetch(
            Exchange._connection,
            self._zeta_group_address,
            utils.default_commitment()
        )
        self.update_margin_params()
    
    def update_margin_params(self):
        if self._zeta_group == None:
            return
        self._margin_params = {
            "future_margin_initial": self.zeta_group.margin_parameters.future_margin_initial,
            "future_margin_maintenance": self.zeta_group.margin_parameters.future_margin_maintenance,
            "option_mark_percentage_long_initial": self.zeta_group.margin_parameters.option_mark_percentage_long_initial,
            "option_spot_percentage_long_initial": self.zeta_group.margin_parameters.option_spot_percentage_long_initial,
            "option_spot_percentage_short_initial": self.zeta_group.margin_parameters.option_spot_percentage_short_initial,
            "option_dynamic_percentage_short_initial": self.zeta_group.margin_parameters.option_dynamic_percentage_short_initial,
            "option_mark_percentage_long_maintenance": self.zeta_group.margin_parameters.option_mark_percentage_long_maintenance,
            "option_spot_percentage_long_maintenance": self.zeta_group.margin_parameters.option_spot_percentage_long_maintenance,
            "option_spot_percentage_short_maintenance": self.zeta_group.margin_parameters.option_spot_percentage_short_maintenance,
            "option_dynamic_percentage_short_maintenance": self.zeta_group.margin_parameters.option_dynamic_percentage_short_maintenance,
            "option_short_put_cap_percentage": self.zeta_group.margin_parameters.option_short_put_cap_percentage,
        }
    def subscribe_zeta_group(self, asset, callback):
        event_emitter = my_client.accounts.zeta_group.ZetaGroup.

    def subscribe_greeks(self):
