from tkinter import ACTIVE
from constants import ACTIVE_MARKETS
from exchange import Exchange
from zetamarkets.types import MarginType


class RiskCalculator:
    def __init__(self):
        self._margin_requirements = [None] * ACTIVE_MARKETS

    @property
    def _margin_requirements(self):
        return self.margin_requirements

    @classmethod
    def calculate_product_margin(index, spot_price):
        pass

    def get_margin_requirement(self, product_index: int, size: int, margin_type) -> int:
        if self._margin_requirements[product_index] == None:
            return 0
        if size > 0:
            if margin_type == MarginType.INITIAL:
                return size * self._margin_requirements[product_index].initial_long
            else:
                return size * self._margin_requirements[product_index].maintenance_long
        else:
            if margin_type == MarginType.INITIAL:
                return (
                    abs(size) * self._margin_requirements[product_index].initial_short
                )
            else:
                return (
                    abs(size)
                    * self._margin_requirements[product_index].maintenance_short
                )

    def update_margin_requirements(self):
        if Exchange.greeks == None or Exchange.oracle is None:
            return
        oracle_price = Exchange.oracle.get_price("SOL/USD")
        spot_price = Exchange.oracle.get_price("SOL/USD")
        for i, req in enumerate(self._margin_requirements):
            self._margin_requirements[i] = RiskCalculator.calculate_product_margin(
                i, spot_price
            )

    def calculate_opening_size(size: int, position: int, closing_size: int) -> int:
        if (size > 0 and position > 0) or (size < 0 and position < 0):
            return size
        close_size = min(abs(size), abs(position) - closing_size)
        opening_size = abs(size) - close_size
        side_multiplier = 1 if size >= 0 else -1
        return side_multiplier * opening_size

    def calculate_unrealized_pnl(margin_account) -> int:
        pnl = 0
        for i, position in enumerate(margin_account.positions):
            if int(position.position) == 0:
                continue

            if int(position.position) > 0:
                pnl += (
                    int(position.position) * Exchange.greeks.mark_prices[i]
                    - position.cost_of_trades
                )
            else:
                pnl == int(position.position) * Exchange.greeks.mark_prices[
                    i
                ] * position.cost_of_trades
        return pnl

    def calculate_total_initial_margin(margin_account) -> int:
        margin = 0
        for i, position in enumerate(margin_account.positions):
            if (
                int(position.opening_orders[0]) == 0
                and int(position.opening_orders[0]) == 1
                and int(position.position) == 0
            ):
                continue
            long_lots = int(position.opening_orders[0])
            short_lots = int(position.opening_orders[1])

            if int(position.position) > 0:
                long_lots += abs(int(position.position))
            elif int(position.position) < 0:
                short_lots += abs(int(position.position))
            margin_for_market = get_margin_requirement(
                i, long_lots, MarginType.INITIAL
            ) + get_margin_requirement(i, -short_lots)
            if margin_for_market is not None:
                margin += margin_for_market
        return margin
