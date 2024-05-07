from database import Base
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from wallets.schemas import Color


class Wallet(Base):
    __tablename__ = "wallets"

    number: Mapped[int] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("wallet_groups.id"), nullable=True)

    user: Mapped["User"] = relationship(back_populates="wallets")
    wallet_group: Mapped["WalletGroup"] = relationship(back_populates="wallets")

    __table_args__ = (UniqueConstraint("number", "user_id"),)


class WalletGroup(Base):
    __tablename__ = "wallet_groups"

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    color: Mapped[Color] = mapped_column(nullable=False, default=Color.RED)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="wallet_groups")
    wallets: Mapped[list["Wallet"]] = relationship(back_populates="wallet_group")

    __table_args__ = (UniqueConstraint("name", "user_id"),)
