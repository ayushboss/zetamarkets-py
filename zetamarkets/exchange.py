from zetamarkets import utils


class Exchange:
    is_initialized = False
    _mint_authority = None
    _state = None
    _serum_authority = None

    def __init__(self, program_id, network, connection, wallet):
        pass

    @classmethod
    def load(cls, program_id, network, connection, opts, wallet, throttle_ms):
        print("Loading Exchange")
        if Exchange.is_initialized:
            raise ("Exchange already initialized")
        [mint_authority, _mint_authority_nonce] = utils.get_mint_authority(program_id)
        [state, _state_nonce] = utils.get_state(program_id)
        [serum_authority, _serum_nonce] = utils.get_serum_authority(program_id)
        _mint_authority = mint_authority
        _state = state
        _serum_authority = serum_authority

        # Load Zeta Group
        [underlying, _underlying_nonce] = utils.get_underlying(program_id, 0)
