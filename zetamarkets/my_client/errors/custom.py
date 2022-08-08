import typing
from anchorpy.error import ProgramError


class DepositOverflow(ProgramError):
    def __init__(self) -> None:
        super().__init__(6000, "Deposit overflow")

    code = 6000
    name = "DepositOverflow"
    msg = "Deposit overflow"


class Unreachable(ProgramError):
    def __init__(self) -> None:
        super().__init__(6001, "Unreachable")

    code = 6001
    name = "Unreachable"
    msg = "Unreachable"


class FailedInitialMarginRequirement(ProgramError):
    def __init__(self) -> None:
        super().__init__(6002, "Failed initial margin requirement")

    code = 6002
    name = "FailedInitialMarginRequirement"
    msg = "Failed initial margin requirement"


class LiquidatorFailedMarginRequirement(ProgramError):
    def __init__(self) -> None:
        super().__init__(6003, "Liquidator failed margin requirement")

    code = 6003
    name = "LiquidatorFailedMarginRequirement"
    msg = "Liquidator failed margin requirement"


class CannotLiquidateOwnAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6004, "Cannot liquidate own account")

    code = 6004
    name = "CannotLiquidateOwnAccount"
    msg = "Cannot liquidate own account"


class CrankInvalidRemainingAccounts(ProgramError):
    def __init__(self) -> None:
        super().__init__(6005, "Invalid cranking remaining accounts")

    code = 6005
    name = "CrankInvalidRemainingAccounts"
    msg = "Invalid cranking remaining accounts"


class IncorrectTickSize(ProgramError):
    def __init__(self) -> None:
        super().__init__(6006, "Incorrect tick size")

    code = 6006
    name = "IncorrectTickSize"
    msg = "Incorrect tick size"


class ZeroPrice(ProgramError):
    def __init__(self) -> None:
        super().__init__(6007, "ZeroPrice")

    code = 6007
    name = "ZeroPrice"
    msg = "ZeroPrice"


class ZeroSize(ProgramError):
    def __init__(self) -> None:
        super().__init__(6008, "ZeroSize")

    code = 6008
    name = "ZeroSize"
    msg = "ZeroSize"


class ZeroWithdrawableBalance(ProgramError):
    def __init__(self) -> None:
        super().__init__(6009, "Zero withdrawable balance")

    code = 6009
    name = "ZeroWithdrawableBalance"
    msg = "Zero withdrawable balance"


class DepositAmountExceeded(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            6010, "Deposit amount exceeds limit and user is not whitelisted"
        )

    code = 6010
    name = "DepositAmountExceeded"
    msg = "Deposit amount exceeds limit and user is not whitelisted"


class WithdrawalAmountExceedsWithdrawableBalance(ProgramError):
    def __init__(self) -> None:
        super().__init__(6011, "Withdrawal amount exceeds withdrawable balance")

    code = 6011
    name = "WithdrawalAmountExceedsWithdrawableBalance"
    msg = "Withdrawal amount exceeds withdrawable balance"


class AccountHasSufficientMarginPostCancels(ProgramError):
    def __init__(self) -> None:
        super().__init__(6012, "Account has sufficient margin post cancels")

    code = 6012
    name = "AccountHasSufficientMarginPostCancels"
    msg = "Account has sufficient margin post cancels"


class OverBankrupt(ProgramError):
    def __init__(self) -> None:
        super().__init__(6013, "Over bankrupt")

    code = 6013
    name = "OverBankrupt"
    msg = "Over bankrupt"


class AccountHasSufficientMargin(ProgramError):
    def __init__(self) -> None:
        super().__init__(6014, "Account has sufficient margin")

    code = 6014
    name = "AccountHasSufficientMargin"
    msg = "Account has sufficient margin"


class UserHasNoActiveOrders(ProgramError):
    def __init__(self) -> None:
        super().__init__(6015, "User has no active orders")

    code = 6015
    name = "UserHasNoActiveOrders"
    msg = "User has no active orders"


class InvalidExpirationInterval(ProgramError):
    def __init__(self) -> None:
        super().__init__(6016, "Invalid expiration interval")

    code = 6016
    name = "InvalidExpirationInterval"
    msg = "Invalid expiration interval"


class ProductMarketsAlreadyInitialized(ProgramError):
    def __init__(self) -> None:
        super().__init__(6017, "Product markets already initialized")

    code = 6017
    name = "ProductMarketsAlreadyInitialized"
    msg = "Product markets already initialized"


class InvalidProductMarketKey(ProgramError):
    def __init__(self) -> None:
        super().__init__(6018, "Invalid product market key")

    code = 6018
    name = "InvalidProductMarketKey"
    msg = "Invalid product market key"


class MarketNotLive(ProgramError):
    def __init__(self) -> None:
        super().__init__(6019, "Market not live")

    code = 6019
    name = "MarketNotLive"
    msg = "Market not live"


class MarketPricingNotReady(ProgramError):
    def __init__(self) -> None:
        super().__init__(6020, "Market pricing not ready")

    code = 6020
    name = "MarketPricingNotReady"
    msg = "Market pricing not ready"


class UserHasRemainingOrdersOnExpiredMarket(ProgramError):
    def __init__(self) -> None:
        super().__init__(6021, "User has remaining orders on expired market")

    code = 6021
    name = "UserHasRemainingOrdersOnExpiredMarket"
    msg = "User has remaining orders on expired market"


class InvalidSeriesExpiration(ProgramError):
    def __init__(self) -> None:
        super().__init__(6022, "Invalid series expiration")

    code = 6022
    name = "InvalidSeriesExpiration"
    msg = "Invalid series expiration"


class InvalidExpiredOrderCancel(ProgramError):
    def __init__(self) -> None:
        super().__init__(6023, "Invalid expired order cancel")

    code = 6023
    name = "InvalidExpiredOrderCancel"
    msg = "Invalid expired order cancel"


class NoMarketsToAdd(ProgramError):
    def __init__(self) -> None:
        super().__init__(6024, "No markets to add")

    code = 6024
    name = "NoMarketsToAdd"
    msg = "No markets to add"


class UserHasUnsettledPositions(ProgramError):
    def __init__(self) -> None:
        super().__init__(6025, "User has unsettled positions")

    code = 6025
    name = "UserHasUnsettledPositions"
    msg = "User has unsettled positions"


class NoMarginAccountsToSettle(ProgramError):
    def __init__(self) -> None:
        super().__init__(6026, "No margin accounts to settle")

    code = 6026
    name = "NoMarginAccountsToSettle"
    msg = "No margin accounts to settle"


class CannotSettleUserWithActiveOrders(ProgramError):
    def __init__(self) -> None:
        super().__init__(6027, "Cannot settle users with active orders")

    code = 6027
    name = "CannotSettleUserWithActiveOrders"
    msg = "Cannot settle users with active orders"


class OrderbookNotEmpty(ProgramError):
    def __init__(self) -> None:
        super().__init__(6028, "Orderbook not empty")

    code = 6028
    name = "OrderbookNotEmpty"
    msg = "Orderbook not empty"


class InvalidNumberOfAccounts(ProgramError):
    def __init__(self) -> None:
        super().__init__(6029, "Invalid number of accounts")

    code = 6029
    name = "InvalidNumberOfAccounts"
    msg = "Invalid number of accounts"


class InvalidMarketAccounts(ProgramError):
    def __init__(self) -> None:
        super().__init__(6030, "Bids or Asks don't match the Market")

    code = 6030
    name = "InvalidMarketAccounts"
    msg = "Bids or Asks don't match the Market"


class ProductStrikeUninitialized(ProgramError):
    def __init__(self) -> None:
        super().__init__(6031, "Product strike uninitialized")

    code = 6031
    name = "ProductStrikeUninitialized"
    msg = "Product strike uninitialized"


class PricingNotUpToDate(ProgramError):
    def __init__(self) -> None:
        super().__init__(6032, "Pricing not up to date")

    code = 6032
    name = "PricingNotUpToDate"
    msg = "Pricing not up to date"


class RetreatsAreStale(ProgramError):
    def __init__(self) -> None:
        super().__init__(6033, "Retreats are stale")

    code = 6033
    name = "RetreatsAreStale"
    msg = "Retreats are stale"


class ProductDirty(ProgramError):
    def __init__(self) -> None:
        super().__init__(6034, "Product dirty")

    code = 6034
    name = "ProductDirty"
    msg = "Product dirty"


class ProductStrikesInitialized(ProgramError):
    def __init__(self) -> None:
        super().__init__(6035, "Product strikes initialized")

    code = 6035
    name = "ProductStrikesInitialized"
    msg = "Product strikes initialized"


class StrikeInitializationNotReady(ProgramError):
    def __init__(self) -> None:
        super().__init__(6036, "Strike initialization not ready")

    code = 6036
    name = "StrikeInitializationNotReady"
    msg = "Strike initialization not ready"


class UnsupportedKind(ProgramError):
    def __init__(self) -> None:
        super().__init__(6037, "Unsupported kind")

    code = 6037
    name = "UnsupportedKind"
    msg = "Unsupported kind"


class InvalidZetaGroup(ProgramError):
    def __init__(self) -> None:
        super().__init__(6038, "Invalid zeta group")

    code = 6038
    name = "InvalidZetaGroup"
    msg = "Invalid zeta group"


class InvalidMarginAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6039, "Invalid margin account")

    code = 6039
    name = "InvalidMarginAccount"
    msg = "Invalid margin account"


class InvalidGreeksAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6040, "Invalid greeks account")

    code = 6040
    name = "InvalidGreeksAccount"
    msg = "Invalid greeks account"


class InvalidSettlementAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6041, "Invalid settlement account")

    code = 6041
    name = "InvalidSettlementAccount"
    msg = "Invalid settlement account"


class InvalidCancelAuthority(ProgramError):
    def __init__(self) -> None:
        super().__init__(6042, "Invalid cancel authority")

    code = 6042
    name = "InvalidCancelAuthority"
    msg = "Invalid cancel authority"


class CannotUpdatePricingAfterExpiry(ProgramError):
    def __init__(self) -> None:
        super().__init__(6043, "Cannot update pricing after expiry")

    code = 6043
    name = "CannotUpdatePricingAfterExpiry"
    msg = "Cannot update pricing after expiry"


class LoadAccountDiscriminatorAlreadySet(ProgramError):
    def __init__(self) -> None:
        super().__init__(6044, "Account discriminator already set")

    code = 6044
    name = "LoadAccountDiscriminatorAlreadySet"
    msg = "Account discriminator already set"


class AccountAlreadyInitialized(ProgramError):
    def __init__(self) -> None:
        super().__init__(6045, "Account already initialized")

    code = 6045
    name = "AccountAlreadyInitialized"
    msg = "Account already initialized"


class GreeksAccountSeedsMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(6046, "Greeks account seeds mismatch")

    code = 6046
    name = "GreeksAccountSeedsMismatch"
    msg = "Greeks account seeds mismatch"


class ZetaGroupAccountSeedsMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(6047, "Zeta group account seeds mismatch")

    code = 6047
    name = "ZetaGroupAccountSeedsMismatch"
    msg = "Zeta group account seeds mismatch"


class MarginAccountSeedsMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(6048, "Margin account seeds mismatch")

    code = 6048
    name = "MarginAccountSeedsMismatch"
    msg = "Margin account seeds mismatch"


class OpenOrdersAccountSeedsMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(6049, "Open orders account seeds mismatch")

    code = 6049
    name = "OpenOrdersAccountSeedsMismatch"
    msg = "Open orders account seeds mismatch"


class MarketNodeAccountSeedsMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(6050, "Market node seeds mismatch")

    code = 6050
    name = "MarketNodeAccountSeedsMismatch"
    msg = "Market node seeds mismatch"


class UserTradingFeeWhitelistAccountSeedsMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(6051, "User trading fee whitelist account seeds mismatch")

    code = 6051
    name = "UserTradingFeeWhitelistAccountSeedsMismatch"
    msg = "User trading fee whitelist account seeds mismatch"


class UserDepositWhitelistAccountSeedsMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(6052, "User deposit whitelist account seeds mismatch")

    code = 6052
    name = "UserDepositWhitelistAccountSeedsMismatch"
    msg = "User deposit whitelist account seeds mismatch"


class MarketIndexesUninitialized(ProgramError):
    def __init__(self) -> None:
        super().__init__(6053, "Market indexes uninitialized")

    code = 6053
    name = "MarketIndexesUninitialized"
    msg = "Market indexes uninitialized"


class MarketIndexesAlreadyInitialized(ProgramError):
    def __init__(self) -> None:
        super().__init__(6054, "Market indexes already initialized")

    code = 6054
    name = "MarketIndexesAlreadyInitialized"
    msg = "Market indexes already initialized"


class CannotGetUnsetStrike(ProgramError):
    def __init__(self) -> None:
        super().__init__(6055, "Cannot get unset strike")

    code = 6055
    name = "CannotGetUnsetStrike"
    msg = "Cannot get unset strike"


class CannotSetInitializedStrike(ProgramError):
    def __init__(self) -> None:
        super().__init__(6056, "Cannot set initialized strike")

    code = 6056
    name = "CannotSetInitializedStrike"
    msg = "Cannot set initialized strike"


class CannotResetUninitializedStrike(ProgramError):
    def __init__(self) -> None:
        super().__init__(6057, "Cannot set initialized strike")

    code = 6057
    name = "CannotResetUninitializedStrike"
    msg = "Cannot set initialized strike"


class CrankMarginAccountNotMutable(ProgramError):
    def __init__(self) -> None:
        super().__init__(6058, "CrankMarginAccountNotMutable")

    code = 6058
    name = "CrankMarginAccountNotMutable"
    msg = "CrankMarginAccountNotMutable"


class InvalidAdminSigner(ProgramError):
    def __init__(self) -> None:
        super().__init__(6059, "InvalidAdminSigner")

    code = 6059
    name = "InvalidAdminSigner"
    msg = "InvalidAdminSigner"


class UserHasActiveOrders(ProgramError):
    def __init__(self) -> None:
        super().__init__(6060, "User still has active orders")

    code = 6060
    name = "UserHasActiveOrders"
    msg = "User still has active orders"


class UserForceCancelInProgress(ProgramError):
    def __init__(self) -> None:
        super().__init__(6061, "User has a force cancel in progress")

    code = 6061
    name = "UserForceCancelInProgress"
    msg = "User has a force cancel in progress"


class FailedPriceBandCheck(ProgramError):
    def __init__(self) -> None:
        super().__init__(6062, "Failed price band check")

    code = 6062
    name = "FailedPriceBandCheck"
    msg = "Failed price band check"


class UnsortedOpenOrdersAccounts(ProgramError):
    def __init__(self) -> None:
        super().__init__(6063, "Unsorted open orders accounts")

    code = 6063
    name = "UnsortedOpenOrdersAccounts"
    msg = "Unsorted open orders accounts"


class AccountNotMutable(ProgramError):
    def __init__(self) -> None:
        super().__init__(6064, "Account not mutable")

    code = 6064
    name = "AccountNotMutable"
    msg = "Account not mutable"


class AccountDiscriminatorMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(6065, "Account discriminator mismatch")

    code = 6065
    name = "AccountDiscriminatorMismatch"
    msg = "Account discriminator mismatch"


class InvalidMarketNodeIndex(ProgramError):
    def __init__(self) -> None:
        super().__init__(6066, "Invalid market node index")

    code = 6066
    name = "InvalidMarketNodeIndex"
    msg = "Invalid market node index"


class InvalidMarketNode(ProgramError):
    def __init__(self) -> None:
        super().__init__(6067, "Invalid market node")

    code = 6067
    name = "InvalidMarketNode"
    msg = "Invalid market node"


class LUTOutOfBounds(ProgramError):
    def __init__(self) -> None:
        super().__init__(6068, "Lut out of bounds")

    code = 6068
    name = "LUTOutOfBounds"
    msg = "Lut out of bounds"


class RebalanceInsuranceInvalidRemainingAccounts(ProgramError):
    def __init__(self) -> None:
        super().__init__(6069, "Rebalance insurance vault with no margin accounts")

    code = 6069
    name = "RebalanceInsuranceInvalidRemainingAccounts"
    msg = "Rebalance insurance vault with no margin accounts"


class InvalidMintDecimals(ProgramError):
    def __init__(self) -> None:
        super().__init__(6070, "Invalid mint decimals")

    code = 6070
    name = "InvalidMintDecimals"
    msg = "Invalid mint decimals"


class InvalidZetaGroupOracle(ProgramError):
    def __init__(self) -> None:
        super().__init__(6071, "Invalid oracle for this zeta group")

    code = 6071
    name = "InvalidZetaGroupOracle"
    msg = "Invalid oracle for this zeta group"


class InvalidZetaGroupDepositMint(ProgramError):
    def __init__(self) -> None:
        super().__init__(6072, "Invalid zeta group deposit mint")

    code = 6072
    name = "InvalidZetaGroupDepositMint"
    msg = "Invalid zeta group deposit mint"


class InvalidZetaGroupRebalanceMint(ProgramError):
    def __init__(self) -> None:
        super().__init__(6073, "Invalid zeta group rebalance insurance vault mint")

    code = 6073
    name = "InvalidZetaGroupRebalanceMint"
    msg = "Invalid zeta group rebalance insurance vault mint"


class InvalidDepositAmount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6074, "Invalid deposit amount")

    code = 6074
    name = "InvalidDepositAmount"
    msg = "Invalid deposit amount"


class InvalidTokenAccountOwner(ProgramError):
    def __init__(self) -> None:
        super().__init__(6075, "Invalid token account owner")

    code = 6075
    name = "InvalidTokenAccountOwner"
    msg = "Invalid token account owner"


class InvalidWithdrawAmount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6076, "Invalid withdraw amount")

    code = 6076
    name = "InvalidWithdrawAmount"
    msg = "Invalid withdraw amount"


class InvalidDepositRemainingAccounts(ProgramError):
    def __init__(self) -> None:
        super().__init__(6077, "Invalid number of remaining accounts in deposit")

    code = 6077
    name = "InvalidDepositRemainingAccounts"
    msg = "Invalid number of remaining accounts in deposit"


class InvalidPlaceOrderRemainingAccounts(ProgramError):
    def __init__(self) -> None:
        super().__init__(6078, "Invalid number of remaining accounts in place order")

    code = 6078
    name = "InvalidPlaceOrderRemainingAccounts"
    msg = "Invalid number of remaining accounts in place order"


class ClientOrderIdCannotBeZero(ProgramError):
    def __init__(self) -> None:
        super().__init__(6079, "ClientOrderIdCannotBeZero")

    code = 6079
    name = "ClientOrderIdCannotBeZero"
    msg = "ClientOrderIdCannotBeZero"


class ZetaGroupHalted(ProgramError):
    def __init__(self) -> None:
        super().__init__(6080, "Zeta group halted")

    code = 6080
    name = "ZetaGroupHalted"
    msg = "Zeta group halted"


class ZetaGroupNotHalted(ProgramError):
    def __init__(self) -> None:
        super().__init__(6081, "Zeta group not halted")

    code = 6081
    name = "ZetaGroupNotHalted"
    msg = "Zeta group not halted"


class HaltMarkPriceNotSet(ProgramError):
    def __init__(self) -> None:
        super().__init__(6082, "Halt mark price not set")

    code = 6082
    name = "HaltMarkPriceNotSet"
    msg = "Halt mark price not set"


class HaltMarketsNotCleaned(ProgramError):
    def __init__(self) -> None:
        super().__init__(6083, "Halt markets not cleaned")

    code = 6083
    name = "HaltMarketsNotCleaned"
    msg = "Halt markets not cleaned"


class HaltMarketNodesNotCleaned(ProgramError):
    def __init__(self) -> None:
        super().__init__(6084, "Halt market nodes not cleaned")

    code = 6084
    name = "HaltMarketNodesNotCleaned"
    msg = "Halt market nodes not cleaned"


class CannotExpireOptionsAfterExpirationThreshold(ProgramError):
    def __init__(self) -> None:
        super().__init__(6085, "Cannot expire options after expiration threshold")

    code = 6085
    name = "CannotExpireOptionsAfterExpirationThreshold"
    msg = "Cannot expire options after expiration threshold"


class PostOnlyInCross(ProgramError):
    def __init__(self) -> None:
        super().__init__(6086, "Post only order in cross")

    code = 6086
    name = "PostOnlyInCross"
    msg = "Post only order in cross"


class FillOrKillNotFullSize(ProgramError):
    def __init__(self) -> None:
        super().__init__(6087, "Fill or kill order was not filled for full size")

    code = 6087
    name = "FillOrKillNotFullSize"
    msg = "Fill or kill order was not filled for full size"


class InvalidOpenOrdersMapOwner(ProgramError):
    def __init__(self) -> None:
        super().__init__(6088, "Invalid open orders map owner")

    code = 6088
    name = "InvalidOpenOrdersMapOwner"
    msg = "Invalid open orders map owner"


class AccountDidNotSerialize(ProgramError):
    def __init__(self) -> None:
        super().__init__(6089, "Failed to serialize the account")

    code = 6089
    name = "AccountDidNotSerialize"
    msg = "Failed to serialize the account"


class OpenOrdersWithNonEmptyPositions(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            6090, "Cannot close open orders account with non empty positions"
        )

    code = 6090
    name = "OpenOrdersWithNonEmptyPositions"
    msg = "Cannot close open orders account with non empty positions"


class CannotCloseNonEmptyMarginAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6091, "Cannot close margin account that is not empty")

    code = 6091
    name = "CannotCloseNonEmptyMarginAccount"
    msg = "Cannot close margin account that is not empty"


class InvalidTagLength(ProgramError):
    def __init__(self) -> None:
        super().__init__(6092, "Invalid tag length")

    code = 6092
    name = "InvalidTagLength"
    msg = "Invalid tag length"


class NakedShortCallIsNotAllowed(ProgramError):
    def __init__(self) -> None:
        super().__init__(6093, "Naked short call is not allowed")

    code = 6093
    name = "NakedShortCallIsNotAllowed"
    msg = "Naked short call is not allowed"


class InvalidSpreadAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6094, "Invalid spread account")

    code = 6094
    name = "InvalidSpreadAccount"
    msg = "Invalid spread account"


class CannotCloseNonEmptySpreadAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6095, "Cannot close non empty spread account")

    code = 6095
    name = "CannotCloseNonEmptySpreadAccount"
    msg = "Cannot close non empty spread account"


class SpreadAccountSeedsMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(6096, "Spread account seeds mismatch")

    code = 6096
    name = "SpreadAccountSeedsMismatch"
    msg = "Spread account seeds mismatch"


class SpreadAccountHasUnsettledPositions(ProgramError):
    def __init__(self) -> None:
        super().__init__(6097, "Spread account seeds mismatch")

    code = 6097
    name = "SpreadAccountHasUnsettledPositions"
    msg = "Spread account seeds mismatch"


class SpreadAccountInvalidExpirySeriesState(ProgramError):
    def __init__(self) -> None:
        super().__init__(6098, "Spread account invalid expiry series state")

    code = 6098
    name = "SpreadAccountInvalidExpirySeriesState"
    msg = "Spread account invalid expiry series state"


class InsufficientFundsToCollateralizeSpreadAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6099, "Insufficient funds to collateralize spread account")

    code = 6099
    name = "InsufficientFundsToCollateralizeSpreadAccount"
    msg = "Insufficient funds to collateralize spread account"


class FailedMaintenanceMarginRequirement(ProgramError):
    def __init__(self) -> None:
        super().__init__(6100, "Failed maintenance margin requirement")

    code = 6100
    name = "FailedMaintenanceMarginRequirement"
    msg = "Failed maintenance margin requirement"


class InvalidMovement(ProgramError):
    def __init__(self) -> None:
        super().__init__(6101, "Invalid movement")

    code = 6101
    name = "InvalidMovement"
    msg = "Invalid movement"


class MovementOnExpiredSeries(ProgramError):
    def __init__(self) -> None:
        super().__init__(6102, "Movement on expired series")

    code = 6102
    name = "MovementOnExpiredSeries"
    msg = "Movement on expired series"


class InvalidMovementSize(ProgramError):
    def __init__(self) -> None:
        super().__init__(6103, "Invalid movement size")

    code = 6103
    name = "InvalidMovementSize"
    msg = "Invalid movement size"


class ExceededMaxPositionMovements(ProgramError):
    def __init__(self) -> None:
        super().__init__(6104, "Exceeded max position movements")

    code = 6104
    name = "ExceededMaxPositionMovements"
    msg = "Exceeded max position movements"


class ExceededMaxSpreadAccountContracts(ProgramError):
    def __init__(self) -> None:
        super().__init__(6105, "Exceeded max spread account contracts")

    code = 6105
    name = "ExceededMaxSpreadAccountContracts"
    msg = "Exceeded max spread account contracts"


class OraclePriceIsInvalid(ProgramError):
    def __init__(self) -> None:
        super().__init__(6106, "Fetched oracle price is invalid")

    code = 6106
    name = "OraclePriceIsInvalid"
    msg = "Fetched oracle price is invalid"


class InvalidUnderlyingMint(ProgramError):
    def __init__(self) -> None:
        super().__init__(6107, "Provided underlying mint address is invalid")

    code = 6107
    name = "InvalidUnderlyingMint"
    msg = "Provided underlying mint address is invalid"


class InvalidReferrerAlias(ProgramError):
    def __init__(self) -> None:
        super().__init__(6108, "Invalid referrer alias - Invalid length")

    code = 6108
    name = "InvalidReferrerAlias"
    msg = "Invalid referrer alias - Invalid length"


class ReferrerAlreadyHasAlias(ProgramError):
    def __init__(self) -> None:
        super().__init__(6109, "Referrer already has alias")

    code = 6109
    name = "ReferrerAlreadyHasAlias"
    msg = "Referrer already has alias"


class InvalidTreasuryMovementAmount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6110, "Invalid treasury movement amount")

    code = 6110
    name = "InvalidTreasuryMovementAmount"
    msg = "Invalid treasury movement amount"


CustomError = typing.Union[
    DepositOverflow,
    Unreachable,
    FailedInitialMarginRequirement,
    LiquidatorFailedMarginRequirement,
    CannotLiquidateOwnAccount,
    CrankInvalidRemainingAccounts,
    IncorrectTickSize,
    ZeroPrice,
    ZeroSize,
    ZeroWithdrawableBalance,
    DepositAmountExceeded,
    WithdrawalAmountExceedsWithdrawableBalance,
    AccountHasSufficientMarginPostCancels,
    OverBankrupt,
    AccountHasSufficientMargin,
    UserHasNoActiveOrders,
    InvalidExpirationInterval,
    ProductMarketsAlreadyInitialized,
    InvalidProductMarketKey,
    MarketNotLive,
    MarketPricingNotReady,
    UserHasRemainingOrdersOnExpiredMarket,
    InvalidSeriesExpiration,
    InvalidExpiredOrderCancel,
    NoMarketsToAdd,
    UserHasUnsettledPositions,
    NoMarginAccountsToSettle,
    CannotSettleUserWithActiveOrders,
    OrderbookNotEmpty,
    InvalidNumberOfAccounts,
    InvalidMarketAccounts,
    ProductStrikeUninitialized,
    PricingNotUpToDate,
    RetreatsAreStale,
    ProductDirty,
    ProductStrikesInitialized,
    StrikeInitializationNotReady,
    UnsupportedKind,
    InvalidZetaGroup,
    InvalidMarginAccount,
    InvalidGreeksAccount,
    InvalidSettlementAccount,
    InvalidCancelAuthority,
    CannotUpdatePricingAfterExpiry,
    LoadAccountDiscriminatorAlreadySet,
    AccountAlreadyInitialized,
    GreeksAccountSeedsMismatch,
    ZetaGroupAccountSeedsMismatch,
    MarginAccountSeedsMismatch,
    OpenOrdersAccountSeedsMismatch,
    MarketNodeAccountSeedsMismatch,
    UserTradingFeeWhitelistAccountSeedsMismatch,
    UserDepositWhitelistAccountSeedsMismatch,
    MarketIndexesUninitialized,
    MarketIndexesAlreadyInitialized,
    CannotGetUnsetStrike,
    CannotSetInitializedStrike,
    CannotResetUninitializedStrike,
    CrankMarginAccountNotMutable,
    InvalidAdminSigner,
    UserHasActiveOrders,
    UserForceCancelInProgress,
    FailedPriceBandCheck,
    UnsortedOpenOrdersAccounts,
    AccountNotMutable,
    AccountDiscriminatorMismatch,
    InvalidMarketNodeIndex,
    InvalidMarketNode,
    LUTOutOfBounds,
    RebalanceInsuranceInvalidRemainingAccounts,
    InvalidMintDecimals,
    InvalidZetaGroupOracle,
    InvalidZetaGroupDepositMint,
    InvalidZetaGroupRebalanceMint,
    InvalidDepositAmount,
    InvalidTokenAccountOwner,
    InvalidWithdrawAmount,
    InvalidDepositRemainingAccounts,
    InvalidPlaceOrderRemainingAccounts,
    ClientOrderIdCannotBeZero,
    ZetaGroupHalted,
    ZetaGroupNotHalted,
    HaltMarkPriceNotSet,
    HaltMarketsNotCleaned,
    HaltMarketNodesNotCleaned,
    CannotExpireOptionsAfterExpirationThreshold,
    PostOnlyInCross,
    FillOrKillNotFullSize,
    InvalidOpenOrdersMapOwner,
    AccountDidNotSerialize,
    OpenOrdersWithNonEmptyPositions,
    CannotCloseNonEmptyMarginAccount,
    InvalidTagLength,
    NakedShortCallIsNotAllowed,
    InvalidSpreadAccount,
    CannotCloseNonEmptySpreadAccount,
    SpreadAccountSeedsMismatch,
    SpreadAccountHasUnsettledPositions,
    SpreadAccountInvalidExpirySeriesState,
    InsufficientFundsToCollateralizeSpreadAccount,
    FailedMaintenanceMarginRequirement,
    InvalidMovement,
    MovementOnExpiredSeries,
    InvalidMovementSize,
    ExceededMaxPositionMovements,
    ExceededMaxSpreadAccountContracts,
    OraclePriceIsInvalid,
    InvalidUnderlyingMint,
    InvalidReferrerAlias,
    ReferrerAlreadyHasAlias,
    InvalidTreasuryMovementAmount,
]
CUSTOM_ERROR_MAP: dict[int, CustomError] = {
    6000: DepositOverflow(),
    6001: Unreachable(),
    6002: FailedInitialMarginRequirement(),
    6003: LiquidatorFailedMarginRequirement(),
    6004: CannotLiquidateOwnAccount(),
    6005: CrankInvalidRemainingAccounts(),
    6006: IncorrectTickSize(),
    6007: ZeroPrice(),
    6008: ZeroSize(),
    6009: ZeroWithdrawableBalance(),
    6010: DepositAmountExceeded(),
    6011: WithdrawalAmountExceedsWithdrawableBalance(),
    6012: AccountHasSufficientMarginPostCancels(),
    6013: OverBankrupt(),
    6014: AccountHasSufficientMargin(),
    6015: UserHasNoActiveOrders(),
    6016: InvalidExpirationInterval(),
    6017: ProductMarketsAlreadyInitialized(),
    6018: InvalidProductMarketKey(),
    6019: MarketNotLive(),
    6020: MarketPricingNotReady(),
    6021: UserHasRemainingOrdersOnExpiredMarket(),
    6022: InvalidSeriesExpiration(),
    6023: InvalidExpiredOrderCancel(),
    6024: NoMarketsToAdd(),
    6025: UserHasUnsettledPositions(),
    6026: NoMarginAccountsToSettle(),
    6027: CannotSettleUserWithActiveOrders(),
    6028: OrderbookNotEmpty(),
    6029: InvalidNumberOfAccounts(),
    6030: InvalidMarketAccounts(),
    6031: ProductStrikeUninitialized(),
    6032: PricingNotUpToDate(),
    6033: RetreatsAreStale(),
    6034: ProductDirty(),
    6035: ProductStrikesInitialized(),
    6036: StrikeInitializationNotReady(),
    6037: UnsupportedKind(),
    6038: InvalidZetaGroup(),
    6039: InvalidMarginAccount(),
    6040: InvalidGreeksAccount(),
    6041: InvalidSettlementAccount(),
    6042: InvalidCancelAuthority(),
    6043: CannotUpdatePricingAfterExpiry(),
    6044: LoadAccountDiscriminatorAlreadySet(),
    6045: AccountAlreadyInitialized(),
    6046: GreeksAccountSeedsMismatch(),
    6047: ZetaGroupAccountSeedsMismatch(),
    6048: MarginAccountSeedsMismatch(),
    6049: OpenOrdersAccountSeedsMismatch(),
    6050: MarketNodeAccountSeedsMismatch(),
    6051: UserTradingFeeWhitelistAccountSeedsMismatch(),
    6052: UserDepositWhitelistAccountSeedsMismatch(),
    6053: MarketIndexesUninitialized(),
    6054: MarketIndexesAlreadyInitialized(),
    6055: CannotGetUnsetStrike(),
    6056: CannotSetInitializedStrike(),
    6057: CannotResetUninitializedStrike(),
    6058: CrankMarginAccountNotMutable(),
    6059: InvalidAdminSigner(),
    6060: UserHasActiveOrders(),
    6061: UserForceCancelInProgress(),
    6062: FailedPriceBandCheck(),
    6063: UnsortedOpenOrdersAccounts(),
    6064: AccountNotMutable(),
    6065: AccountDiscriminatorMismatch(),
    6066: InvalidMarketNodeIndex(),
    6067: InvalidMarketNode(),
    6068: LUTOutOfBounds(),
    6069: RebalanceInsuranceInvalidRemainingAccounts(),
    6070: InvalidMintDecimals(),
    6071: InvalidZetaGroupOracle(),
    6072: InvalidZetaGroupDepositMint(),
    6073: InvalidZetaGroupRebalanceMint(),
    6074: InvalidDepositAmount(),
    6075: InvalidTokenAccountOwner(),
    6076: InvalidWithdrawAmount(),
    6077: InvalidDepositRemainingAccounts(),
    6078: InvalidPlaceOrderRemainingAccounts(),
    6079: ClientOrderIdCannotBeZero(),
    6080: ZetaGroupHalted(),
    6081: ZetaGroupNotHalted(),
    6082: HaltMarkPriceNotSet(),
    6083: HaltMarketsNotCleaned(),
    6084: HaltMarketNodesNotCleaned(),
    6085: CannotExpireOptionsAfterExpirationThreshold(),
    6086: PostOnlyInCross(),
    6087: FillOrKillNotFullSize(),
    6088: InvalidOpenOrdersMapOwner(),
    6089: AccountDidNotSerialize(),
    6090: OpenOrdersWithNonEmptyPositions(),
    6091: CannotCloseNonEmptyMarginAccount(),
    6092: InvalidTagLength(),
    6093: NakedShortCallIsNotAllowed(),
    6094: InvalidSpreadAccount(),
    6095: CannotCloseNonEmptySpreadAccount(),
    6096: SpreadAccountSeedsMismatch(),
    6097: SpreadAccountHasUnsettledPositions(),
    6098: SpreadAccountInvalidExpirySeriesState(),
    6099: InsufficientFundsToCollateralizeSpreadAccount(),
    6100: FailedMaintenanceMarginRequirement(),
    6101: InvalidMovement(),
    6102: MovementOnExpiredSeries(),
    6103: InvalidMovementSize(),
    6104: ExceededMaxPositionMovements(),
    6105: ExceededMaxSpreadAccountContracts(),
    6106: OraclePriceIsInvalid(),
    6107: InvalidUnderlyingMint(),
    6108: InvalidReferrerAlias(),
    6109: ReferrerAlreadyHasAlias(),
    6110: InvalidTreasuryMovementAmount(),
}


def from_code(code: int) -> typing.Optional[CustomError]:
    maybe_err = CUSTOM_ERROR_MAP.get(code)
    if maybe_err is None:
        return None
    return maybe_err
