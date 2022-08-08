import typing
from dataclasses import dataclass
from base64 import b64decode
from solana.publickey import PublicKey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
import borsh_construct as borsh
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from anchorpy.borsh_extension import BorshPubkey
from ..program_id import PROGRAM_ID
from .. import types


class ZetaGroupJSON(typing.TypedDict):
    nonce: int
    vault_nonce: int
    insurance_vault_nonce: int
    front_expiry_index: int
    halt_state: types.halt_state.HaltStateJSON
    underlying_mint: str
    oracle: str
    greeks: str
    pricing_parameters: types.pricing_parameters.PricingParametersJSON
    margin_parameters: types.margin_parameters.MarginParametersJSON
    products: list[types.product.ProductJSON]
    products_padding: list[types.product.ProductJSON]
    expiry_series: list[types.expiry_series.ExpirySeriesJSON]
    expiry_series_padding: list[types.expiry_series.ExpirySeriesJSON]
    total_insurance_vault_deposits: int
    asset: types.asset.AssetJSON
    padding: list[int]


@dataclass
class ZetaGroup:
    discriminator: typing.ClassVar = b"y\x11\xd2km\xeb\x0e\x0c"
    layout: typing.ClassVar = borsh.CStruct(
        "nonce" / borsh.U8,
        "vault_nonce" / borsh.U8,
        "insurance_vault_nonce" / borsh.U8,
        "front_expiry_index" / borsh.U8,
        "halt_state" / types.halt_state.HaltState.layout,
        "underlying_mint" / BorshPubkey,
        "oracle" / BorshPubkey,
        "greeks" / BorshPubkey,
        "pricing_parameters" / types.pricing_parameters.PricingParameters.layout,
        "margin_parameters" / types.margin_parameters.MarginParameters.layout,
        "products" / types.product.Product.layout[46],
        "products_padding" / types.product.Product.layout[92],
        "expiry_series" / types.expiry_series.ExpirySeries.layout[2],
        "expiry_series_padding" / types.expiry_series.ExpirySeries.layout[4],
        "total_insurance_vault_deposits" / borsh.U64,
        "asset" / types.asset.layout,
        "padding" / borsh.U8[1062],
    )
    nonce: int
    vault_nonce: int
    insurance_vault_nonce: int
    front_expiry_index: int
    halt_state: types.halt_state.HaltState
    underlying_mint: PublicKey
    oracle: PublicKey
    greeks: PublicKey
    pricing_parameters: types.pricing_parameters.PricingParameters
    margin_parameters: types.margin_parameters.MarginParameters
    products: list[types.product.Product]
    products_padding: list[types.product.Product]
    expiry_series: list[types.expiry_series.ExpirySeries]
    expiry_series_padding: list[types.expiry_series.ExpirySeries]
    total_insurance_vault_deposits: int
    asset: types.asset.AssetKind
    padding: list[int]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: PublicKey,
        commitment: typing.Optional[Commitment] = None,
    ) -> typing.Optional["ZetaGroup"]:
        resp = await conn.get_account_info(address, commitment=commitment)
        info = resp["result"]["value"]
        if info is None:
            return None
        if info["owner"] != str(PROGRAM_ID):
            raise ValueError("Account does not belong to this program")
        bytes_data = b64decode(info["data"][0])
        return cls.decode(bytes_data)

    @classmethod
    async def fetch_multiple(
        cls,
        conn: AsyncClient,
        addresses: list[PublicKey],
        commitment: typing.Optional[Commitment] = None,
    ) -> typing.List[typing.Optional["ZetaGroup"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["ZetaGroup"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != PROGRAM_ID:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "ZetaGroup":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = ZetaGroup.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            nonce=dec.nonce,
            vault_nonce=dec.vault_nonce,
            insurance_vault_nonce=dec.insurance_vault_nonce,
            front_expiry_index=dec.front_expiry_index,
            halt_state=types.halt_state.HaltState.from_decoded(dec.halt_state),
            underlying_mint=dec.underlying_mint,
            oracle=dec.oracle,
            greeks=dec.greeks,
            pricing_parameters=types.pricing_parameters.PricingParameters.from_decoded(
                dec.pricing_parameters
            ),
            margin_parameters=types.margin_parameters.MarginParameters.from_decoded(
                dec.margin_parameters
            ),
            products=list(
                map(lambda item: types.product.Product.from_decoded(item), dec.products)
            ),
            products_padding=list(
                map(
                    lambda item: types.product.Product.from_decoded(item),
                    dec.products_padding,
                )
            ),
            expiry_series=list(
                map(
                    lambda item: types.expiry_series.ExpirySeries.from_decoded(item),
                    dec.expiry_series,
                )
            ),
            expiry_series_padding=list(
                map(
                    lambda item: types.expiry_series.ExpirySeries.from_decoded(item),
                    dec.expiry_series_padding,
                )
            ),
            total_insurance_vault_deposits=dec.total_insurance_vault_deposits,
            asset=types.asset.from_decoded(dec.asset),
            padding=dec.padding,
        )

    def to_json(self) -> ZetaGroupJSON:
        return {
            "nonce": self.nonce,
            "vault_nonce": self.vault_nonce,
            "insurance_vault_nonce": self.insurance_vault_nonce,
            "front_expiry_index": self.front_expiry_index,
            "halt_state": self.halt_state.to_json(),
            "underlying_mint": str(self.underlying_mint),
            "oracle": str(self.oracle),
            "greeks": str(self.greeks),
            "pricing_parameters": self.pricing_parameters.to_json(),
            "margin_parameters": self.margin_parameters.to_json(),
            "products": list(map(lambda item: item.to_json(), self.products)),
            "products_padding": list(
                map(lambda item: item.to_json(), self.products_padding)
            ),
            "expiry_series": list(map(lambda item: item.to_json(), self.expiry_series)),
            "expiry_series_padding": list(
                map(lambda item: item.to_json(), self.expiry_series_padding)
            ),
            "total_insurance_vault_deposits": self.total_insurance_vault_deposits,
            "asset": self.asset.to_json(),
            "padding": self.padding,
        }

    @classmethod
    def from_json(cls, obj: ZetaGroupJSON) -> "ZetaGroup":
        return cls(
            nonce=obj["nonce"],
            vault_nonce=obj["vault_nonce"],
            insurance_vault_nonce=obj["insurance_vault_nonce"],
            front_expiry_index=obj["front_expiry_index"],
            halt_state=types.halt_state.HaltState.from_json(obj["halt_state"]),
            underlying_mint=PublicKey(obj["underlying_mint"]),
            oracle=PublicKey(obj["oracle"]),
            greeks=PublicKey(obj["greeks"]),
            pricing_parameters=types.pricing_parameters.PricingParameters.from_json(
                obj["pricing_parameters"]
            ),
            margin_parameters=types.margin_parameters.MarginParameters.from_json(
                obj["margin_parameters"]
            ),
            products=list(
                map(lambda item: types.product.Product.from_json(item), obj["products"])
            ),
            products_padding=list(
                map(
                    lambda item: types.product.Product.from_json(item),
                    obj["products_padding"],
                )
            ),
            expiry_series=list(
                map(
                    lambda item: types.expiry_series.ExpirySeries.from_json(item),
                    obj["expiry_series"],
                )
            ),
            expiry_series_padding=list(
                map(
                    lambda item: types.expiry_series.ExpirySeries.from_json(item),
                    obj["expiry_series_padding"],
                )
            ),
            total_insurance_vault_deposits=obj["total_insurance_vault_deposits"],
            asset=types.asset.from_json(obj["asset"]),
            padding=obj["padding"],
        )
