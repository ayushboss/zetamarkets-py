import json
from zetamarkets.constants import IDL_PATH, CLUSTER_URLS
from zetamarkets.oracle import Oracle
# from zetamarkets.risk import RiskCalculator
from zetamarkets import utils,events
from typing import Callable
from anchorpy import Provider, Idl, Program
from solana.publickey import PublicKey


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
    is_initialized = False

    def __init__(self, program_id, network, connection, wallet):
        # TODO: Come back to this later and see if relevant
        pass

    def _init(self, program_id, network, connection, wallet, opts):
        self._provider = Provider(connection, wallet)
        self._network = network
        self._oracle = Oracle(self._network, connection)
        with IDL_PATH.open() as f:
            raw_idl = json.load(f)
        idl = Idl.from_json(raw_idl)
        self._program = Program(idl, program_id)
        # self._risk_calculator = RiskCalculator()

        self._last_poll_timestamp = 0
        self._zetagroup = None
        self._state_address = None
        self._is_initialized = False

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

    @classmethod
    async def load(cls, program_id: PublicKey, network, connection, opts, wallet, throttle_ms):
        print("Loading Exchange")
        exchange = Exchange(program_id, network, connection, wallet)
        if exchange.is_initialized:
            raise ("Exchange already initialized")
        exchange._init(program_id, network, connection, wallet, opts)
        [mint_authority, _mint_authority_nonce] = utils.get_mint_authority(program_id)
        [state, _state_nonce] = utils.get_state(program_id)
        [serum_authority, _serum_nonce] = utils.get_serum_authority(program_id)
        _mint_authority = mint_authority
        _state = state
        _serum_authority = serum_authority

        # Load Zeta Group
        [underlying, _underlying_nonce] = utils.get_underlying(program_id, 0)
        exchange._program.account.get('Underlying').provider.connection._provider.endpoint_uri = CLUSTER_URLS[network]
        underlying_account = await exchange._program.account.get('Underlying').fetch(PublicKey(underlying))
        # Provider not set
        [zeta_group, _zeta_group_nonce] = utils.get_zeta_group(program_id, underlying_account.mint)
        exchange._zeta_group_address = zeta_group

        # exchange.subscribe_oracle(callback)
        # await exchange.update_state()
        await exchange.update_zeta_group()
        [vault_address, _vault_nonce] = utils.get_vault(exchange._program.program_id, zeta_group)
        [insurance_vault_address, _insurance_nonce_nonce] = utils.get_zeta_insurance_vault(exchange._program.program_id, exchange._zeta_group_address)



    async def _subscribe_oracle(self, callback: Callable):
        def _subscribe_oracle_helper(price):
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
        raise("Not implemented")
