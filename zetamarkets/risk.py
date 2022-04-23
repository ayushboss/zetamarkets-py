from constants import ACTIVE_MARKETS
from exchange import Exchange
from zetamarkets.types import MarginType, Kind


class RiskCalculator:
    def __init__(self):
        self._margin_requirements = [None] * ACTIVE_MARKETS

    @property
    def _margin_requirements(self):
        return self.margin_requirements

    @staticmethod
    def calculate_future_margin(spot_price: int):
        initial = spot_price * Exchange.margin_params.future_margin_initial
        maintenance = spot_price * Exchange.margin_params.future_margin_maintenance
        return {
            "initialLong": initial,
            "initialShort": initial,
            "maintenanceLong": maintenance,
            "maintenanceShort": maintenance,
        }

    @staticmethod
    def calculate_short_option_margin(
        spot_price: int, otm_amount: int, margin_type
    ) -> int:
        base_percentage_short = (
            Exchange.margin_params.option_dynamic_percentage_short_initial
            if margin_type == MarginType.Initial
            else Exchange.margin_params.option_dynamic_percentage_short_maintenance
        )
        spot_price_percentage_short = spot_price * (
            base_percentage_short - otm_amount / spot_price
        )
        dynamic_margin = spot_price * (base_percentage_short - otm_amount / spot_price)
        min_margin = spot_price * spot_price_percentage_short
        return max(dynamic_margin, min_margin)

    @staticmethod
    def calculate_long_option_margin(
        spot_price: int, mark_price: int, margin_type
    ) -> int:
        mark_percentage_long = (
            Exchange.margin_params.option_mark_percentage_long_initial
            if margin_type == MarginType.Initial
            else Exchange.margin_params.option_mark_percentage_long_maintenance
        )
        spot_percentage_long = (
            Exchange.margin_params.option_spot_percentage_long_initial
            if margin_type == MarginType.Initial
            else Exchange.margin_params.option_spot_percentage_long_maintenance
        )
        return min(mark_price * mark_percentage_long, spot_price * spot_percentage_long)

    @classmethod
    def calculate_product_margin(product_index: int, spot_price: int):
        market = Exchange.markets.markets[product_index]
        if market.strike == None:
            return None
        kind = market.kind
        strike = market.strike
        mark_price = Exchange.greeks.mark_prices[product_index]
        if kind == Kind.FUTURE:
            return RiskCalculator.calculate_future_margin(spot_price)
        elif kind == Kind.CALL or kind == Kind.PUT:
            return RiskCalculator.calculate_option_margin(
                spot_price, mark_price, kind, strike
            )

    def get_margin_requirement(self, product_index: int, size: int, margin_type) -> int:
        if self._margin_requirements[product_index] == None:
            return 0
        if size > 0:
            if margin_type == MarginType.Initial:
                return size * self._margin_requirements[product_index].initial_long
            else:
                return size * self._margin_requirements[product_index].maintenance_long
        else:
            if margin_type == MarginType.Initial:
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

    @staticmethod
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

    def calculate_total_initial_margin(self, margin_account) -> int:
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
            margin_for_market = self.get_margin_requirement(
                i, long_lots, MarginType.Initial
            ) + self.get_margin_requirement(i, -short_lots)
            if margin_for_market is not None:
                margin += margin_for_market
        return margin

    def calculate_total_maintenance_margin(self, margin_account) -> int:
        margin = 0
        for index, position in enumerate(margin_account.positions):
            if int(position.position) == 0:
                continue
            position_margin = self.get_margin_requirement(
                index, int(position.position), MarginType.Maintenance
            )
            if position_margin is not None:
                margin += position_margin
        return margin

    def calculate_total_maintenance_margin_including_orders(
        self, margin_account
    ) -> int:
        margin = 0
        for i, position in enumerate(margin_account.position):
            if (
                int(position.opening_orders[0]) == 0
                and int(position.opening_orders[1]) == 0
                and int(position.position) == 0
            ):
                continue
            long_lots = int(position.opening_orders[0])
            short_lots = int(position.opening_orders[1])

            if int(position.position) > 0:
                long_lots += abs(int(position.position))
            elif int(position.position) < 0:
                short_lots += abs(int(position.position))

            margin_for_market = self.get_margin_requirement(
                i, long_lots, MarginType.Maintenance
            ) + self.get_margin_requirement(i, -short_lots, MarginType.Maintenance)
            if margin_for_market is not None:
                margin += margin_for_market
        return margin

    def get_margin_account_state(self, margin_account):
        balance = margin_account.balance
        unrealized_pnl = self.calculate_unrealized_pnl(margin_account)
        initial_margin = self.calculate_total_initial_margin(margin_account)
        maintenance_margin = self.calculate_total_maintenance_margin(margin_account)
        available_balance_initial = balance + unrealized_pnl - initial_margin
        available_balance_maintenance = balance + unrealized_pnl - maintenance_margin
        return {
            "balance": balance,
            "initialMargin": initial_margin,
            "maintenanceMargin": maintenance_margin,
            "unrealizedPnl": unrealized_pnl,
            "availableBalanceInitial": available_balance_initial,
            "availableBalanceMaintenance": available_balance_maintenance,
        }

    @staticmethod
    def calculate_liquidation_price(
        account_balance: int,
        margin_requirement: int,
        unrealized_pnl: int,
        mark_price: int,
        position: int,
    ):
        if position == 0:
            return 0
        available_balance = account_balance - margin_requirement + unrealized_pnl

        return mark_price - available_balance / position

    @staticmethod
    def calculate_otm_amount(kind, strike: int, spot_price: int) -> int:
        if kind == Kind.CALL:
            return max(0, strike - spot_price)
        elif kind == Kind.PUT:
            return max(0, spot_price - strike)
        else:
            raise Exception("Unsupported kind for OTM amount.")

    @staticmethod
    def calculate_option_margin(spot_price, mark_price, kind, strike):
        otm_amount = RiskCalculator.calculate_otm_amount(kind, strike, spot_price)
        initial_long = RiskCalculator.calculate_long_option_margin(
            spot_price, mark_price, MarginType.INITIAL
        )
        initial_short = RiskCalculator.calculate_short_option_margin(
            spot_price, otm_amount, MarginType.INITIAL
        )
        maintainance_long = RiskCalculator.calculate_long_option_margin(
            spot_price, mark_price, MarginType.MAINTENANCE
        )
        maintenance_short = RiskCalculator.calculate_short_option_margin(
            spot_price, otm_amount, MarginType.MAINTENANCE
        )
        # TODO: Add return values
        return {}
