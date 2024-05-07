from decimal import Decimal
import re
from enum import Enum
from typing import List

from pydantic import BaseModel, Field, PositiveInt, validator


class Color(str, Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


class WalletSchema(BaseModel):
    id: int
    number: int = Field(examples=["1"])
    address: str = Field(examples=["0x1234567890123456789012345678901234567890"])
    group_id: int | None = Field(examples=[1], default=None)


class WalletCreateSchema(BaseModel):
    address: str = Field(examples=["0x1234567890123456789012345678901234567890"])

    @validator("address")
    def validate_address(cls, address: str) -> str:
        address_pattern = re.compile(r"^0x[a-fA-F0-9]{40}$")

        if not address_pattern.match(address):
            raise ValueError("Invalid wallet address format")

        return address


class WalletPutSchema(BaseModel):
    id: PositiveInt
    number: int = Field(examples=["1"], default=None)
    address: str = Field(examples=["0x1234567890123456789012345678901234567890"])
    group_id: PositiveInt | None = Field(examples=[1])


class WalletPatchSchema(BaseModel):
    id: PositiveInt
    number: int | None = Field(examples=["1"], default=None)
    address: str | None = Field(
        examples=["0x1234567890123456789012345678901234567890"], default=None
    )
    group_id: PositiveInt | None = Field(examples=[1], default=None)


class WalletDeleteSchema(BaseModel):
    id: PositiveInt


class WalletGroupSchema(BaseModel):
    id: int
    name: str = Field(examples=["Group 1"])
    color: Color = Field(examples=["red"])


class WalletGroupCreateSchema(BaseModel):
    name: str = Field(examples=["Group 1"])
    color: Color | None = Field(examples=["red"], default=None)


class WalletGroupPutSchema(BaseModel):
    name: str = Field(examples=["Group 1"])
    color: Color = Field(examples=["red"])


class WalletGroupPatchSchema(BaseModel):
    id: PositiveInt
    name: str | None = Field(examples=["Group 1"], default=None)
    color: Color | None = Field(examples=["red"], default=None)


class ChainSchema(BaseModel):
    name: str = Field(examples=["Ethereum"])
    symbol: str = Field(examples=["ETH"])
    logo: str = Field(examples=["https://example.com/logo.png"])


class ChainsSchema(BaseModel):
    chains: List[ChainSchema]


class WalletBalanceSchema(BaseModel):
    address: str = Field(examples=["0x1234567890123456789012345678901234567890"])
    native_balance: int | float = Field(examples=[5])
    native_in_usd: int | float = Field(examples=[1000])
    usdt_balance: int | float | None = Field(examples=[50.167])
    usdc_balance: int | float | None = Field(examples=[0.000902])


class ChainBalanceSchema(BaseModel):
    chain: str
    balance: WalletBalanceSchema
