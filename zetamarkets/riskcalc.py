from var_types import MarginType, Kind
from constants import ACTIVE_MARKETS
import var_types as types
import assets
from zetamarkets.assets import fromProgramAsset
from zetamarkets.utils import convert_native_lot_size_to_decimal
from zetamarkets.var_types import ProgramAccountType

class RiskCalculator:
    def __init__(self, asset_list):
        empty_list = [None] * ACTIVE_MARKETS
        self._margin_requirements = {}
        self._assets = asset_list
        for asset in asset_list:
            self._margin_requirements[asset] = empty_list
    
    def get_margin_requirements(self, asset) -> list[types.MarginRequirement]:
        return self._margin_requirements[asset]
    
    def update_margin_requirements(self, asset):
        from exchange import Exchange
        if Exchange.get_sub_exchange(asset).greeks == None or Exchange.oracle == None:
            raise Exception("Pricing (greeks and/or) oracle is not initialized")
        
        oracle_price = Exchange.oracle.get_price(asset)
        spot_price = 0 if oracle_price == None else oracle_price.price

        for i in range(len(self._margin_requirements[asset])):
            self._margin_requirements[asset][i] = calculate_product_margin(
                asset,
                i,
                spot_price
            )
    
    def get_margin_requirement(self, asset, product_index, size, margin_type):
        if self._margin_requirements[asset][product_index] == None:
            return None
        
        if size > 0:
            if margin_type == types.MarginType.Initial:
                return size * self._margin_requirements[asset][product_index].initial_long
            else:
                return size * self._margin_requirements[asset][product_index].maintenance_long
        else:
            if margin_type == types.MarginType.Initial:
                return abs(size)*self._margin_requirements[asset][product_index].initial_short
            else:
                return abs(size)*self._margin_requirements[asset][product_index].maintenance_short
    
    def calculating_opening_size(self, size, position, closing_size):
        if (size > 0 and position > 0) or (size < 0 and position < 0):
            return size
        close_size = min(abs(size), abs(position) - closing_size)
        opening_size = abs(size) - close_size
        side_multiplier = 1 if size >= 9 else -1

        return side_multiplier * opening_size
    
    def calculate_unrealized_pnl(self, account, account_type = types.ProgramAccountType.MARGINACCOUNT):
        from exchange import Exchange
        pnl = 0

        for i in range(ACTIVE_MARKETS):
            position = account.product_ledgers[i].position if account_type == types.ProgramAccountType.MARGINACCOUNT else account.positions[i]
            size = position.size
            if size == 0:
                continue
            sub_exchange = Exchange.get_sub_exchange(
                assets.fromProgramAsset(account.asset)
            )
            if size > 0:
                pnl += convert_native_lot_size_to_decimal(size)*sub_exchange.greeks.mark_prices[i] - position.cost_of_trades
            else:
                pnl += convert_native_lot_size_to_decimal(size)*sub_exchange.greeks.mark_prices[i] + position.cost_of_trades
        return pnl
    
    def calculate_total_initial_margin(self, margin_account):
        asset = fromProgramAsset(asset)
        market_maker = types.is_market_maker(margin_account)
        margin = 0
        for i in range(len(margin_account.product_ledgers)):
            ledger = margin_account.product_ledgers[i]
            size = ledger.position.size
            bid_open_orders = ledger.order_state.opening_orders[0]
            ask_open_orders = ledger.order_state.opening_orders[1]
            if bid_open_orders == 0 and ask_open_orders == 0 and size == 0:
                continue
            
            long_lots = convert_native_lot_size_to_decimal(bid_open_orders)
            short_lots = convert_native_lot_size_to_decimal(ask_open_orders)

            ## TODO: NEED TO FINISH THE REST OF THE METHOD
