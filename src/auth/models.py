from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_verified: Mapped[bool] = mapped_column(nullable=False, default=False)

    wallets: Mapped[list["Wallet"]] = relationship(back_populates="user")
    wallet_groups: Mapped[list["WalletGroup"]] = relationship(back_populates="user")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    sub: Mapped[int] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    fingerprint: Mapped[str] = mapped_column(nullable=False)
    refresh_token_uuid: Mapped[str] = mapped_column(nullable=False)
    iat: Mapped[int] = mapped_column(nullable=False)
    exp: Mapped[int] = mapped_column(nullable=False)
