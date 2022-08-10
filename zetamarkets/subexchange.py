# from assets import Asset, assetToName
# from solana.publickey import PublicKey
# from solana.transaction import Transaction, TransactionInstruction, TransactionSignature
# import constants
# import utils
# from exchange import Exchange
# from zetamarkets.markets import ZetaGroupMarkets
# import program_instructions as instructions
# import var_types as types

# class SubExchange:
    # def __init__(self):
    #     self.__isSetup = False
    #     self.__isInitialized = False
    #     self.__zetaGroup = None ### NEED TO IMPLEMENT THE ZETAGROUP CLASS
    #     self.__asset = Asset.UNDEFINED
    #     self.__zetaGroupAddress = PublicKey("0")
    #     self.__vaultAddress = PublicKey("0")
    #     self.__insuranceVaultAddress = PublicKey("0")
    #     self.__socializedLossAccountAddress = PublicKey("0")
    #     self.__markets = None ### NEED TO IMPLEMENT THE ZETA GROUP MARKETS CLASS
    #     self.__eventEmitters = []
    #     self.__greeks = None ### NEED TO IMPLEMENT GREEKS CLASS
    #     self.__greeksAddress = PublicKey("0")
    #     self.__marginParams = None ### NEED TO IMPLEMENT WHATEVER THIS IS

#     def isSetup(self):
#         return self.__isSetup

#     def isInitialized(self):
#         return self.__isInitialized

#     def getZetaGroup(self):
#         return self.__zetaGroup
    
#     def getAsset(self):
#         return self.__asset
    
#     def getZetaGroupAddress(self):
#         return self.__zetaGroupAddress
    
#     def getVaultAddress(self):
#         return self.__vaultAddress
    
#     def getInsuranceVaultAddress(self):
#         return self.__insuranceVaultAddress
    
#     def getSocializedLossAccountAddress(self):
#         return self.__socializedLossAccountAddress

#     def getMarkets(self):
#         return self.__markets
    
#     def getEventEmitters(self):
#         return self.__eventEmitters

#     def getGreeks(self):
#         return self.__greeks
    
#     def getGreeksAddress(self):
#         return self.__greeksAddress
    
#     def getMarginParams(self):
#         return self.__marginParams

#     async def initialize(self, asset):
#         if self.isSetup():
#             raise Exception("SubExchange already initialized")
        
#         self.__asset = asset
#         underlyingMint = constants.MINTS[assetToName(asset)]

#         zetaGroup, __zetaGroupNonce = await utils.get_zeta_group(
#             Exchange.program_id,
#             underlyingMint
#         )

#         self.__zetaGroupAddress = zetaGroup

#         greeks, _greeksNonce = await utils.get_greeks(
#             Exchange.program_id,
#             self.__zetaGroupAddress
#         )

#         self.__greeksAddress = greeks

#         vault_address, _vault_nonce = await utils.get_vault( ### NEED TO IMPLEMENT GET VAULT FUNCTION
#             Exchange.program_id,
#             self.__zetaGroupAddress
#         )

#         insuranceVaultAddress, _insuranceNonce = await utils.get_zeta_insurance_vault(
#             Exchange.program_id,
#             self.__zetaGroupAddress
#         )

#         socializedLossAccount, _socializedLossAccountNonce = await utils.get_socialized_loss_account(
#             Exchange.program_id,
#             self.__zetaGroupAddress
#         )

#         self.__vaultAddress = vault_address
#         self.__insuranceVaultAddress = insuranceVaultAddress
#         self.__socializedLossAccountAddress = socializedLossAccount

#         self.__isSetup = True

#     async def load(self, asset, program_id, network, opts, throttleMs, callback):
#         print("Loading " + assetToName(asset) + " subexchange")
#         if self.isInitialized(): raise Exception("SubExchange already loaded.")

#         await self.updateZetaGroup() ### NEED TO IMPLEMENT THE UPDATE ZETA GROUP METHOD

#         self.__markets = await ZetaGroupMarkets.load(self.__asset, opts, 0)
#         if self.__zetaGroup.products[self.__zetaGroup.products.length - 1].market == PublicKey(0):
#             raise Exception("Zeta group markets are uninitialized")
        
#         self.__markets = await ZetaGroupMarkets.load(self.__asset, opts, throttleMs)
        
#         ### TODO: WE NEED TO FIGURE OUT THE ANCHOR PROGRAM THROUGH THE EXCHANGE CLASS AND THEN COME BACK
#         # self.__greeks = await Exchange.progra 
#         Exchange.risk_calculator.update_margin_requirements(self.__asset)

#         self.subscribe_zeta_group(asset, callback)
#         self.subscribe_greeks(asset, callback)

#         self.__isInitialized = True

#         print(assetToName(asset) + " SubExchange loaded")
    
#     async def initialize_market_nodes(self, zeta_group):
#         for index in range(constants.ACTIVE_MARKETS):
#             tx = Transaction().add(
#                 await instructions.initialize_market_node_ix(self.getAsset(), index)
#             )
#             await utils.process_transaction(Exchange.provider, tx)

#     async def updatePricingParameters(self, args):
#         tx = Transaction().add(
#             instructions.update_pricing_parameters_ix(
#                 self.getAsset(),
#                 args,
#                 Exchange.provider.wallet.public_key
#             )
#         )
#         await utils.process_transaction(Exchange.provider, tx)
#         await self.update_zeta_group()
    
#     async def updateMarginParameters(self, args):
#         tx = Transaction().add(
#             instructions.update_margin_parameters_ix(
#                 self.getAsset(),
#                 args,
#                 Exchange.provider.wallet.public_key
#             )
#         )
#         await utils.process_transaction(Exchange.provider, tx)
#         await self.update_zeta_group()
    
#     async def updateVolatilityNodes(self, nodes):
#         if len(nodes) != constants.VOLATILITY_POINTS: 
#             raise Exception("Invalid number of nodes. Expected " + str(constants.VOLATILITY_POINTS))
        
#         tx = Transaction().add(
#             instructions.update_volatility_nodes_ix(
#                 self.get_asset(),
#                 nodes,
#                 Exchange.provider.wallet.public_key
#             )
#         )
#         await utils.process_transaction(Exchange.provider, tx)
    
#     async def initializeZetaMarkets(self):
#         marketIndexes, marketIndexesNonce = await utils.get_market_indexes(
#             Exchange.program_id,
#             self.__zetaGroupAddress
#         )
#         print("Initializing market indexes.")
#         tx = Transaction().add(
#             instructions.initialize_market_indexes_ix(
#                 self.__asset,
#                 marketIndexes,
#                 marketIndexesNonce
#             )
#         )
#         try:
#             await utils.process_transaction(
#                 Exchange.get_mark_price(),
#                 tx,
#                 [],
#                 utils.default_commitment(),
#                 Exchange._use_ledger
#             )
#         except:
#             print("An exception occurred")
        
#         tx2 = Transaction().add(
#             instructions.add_market_indexes_ix(self.__asset, marketIndexes)
#         )
