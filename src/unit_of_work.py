from abc import ABC, abstractmethod
from typing import Self

from auth.repository import RefreshTokenRepository, UserRepository
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from wallets.repository import WalletGroupRepository, WalletRepository


class AbstractUnitOfWork(ABC):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self) -> Self:
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory
        self._user_repo = None
        self._refresh_token_repo = None
        self._wallet_repo = None
        self._wallet_group_repo = None

    @property
    def user(self) -> UserRepository:
        if self._user_repo is None:
            self._user_repo = UserRepository(self._session)

        return self._user_repo

    @property
    def refresh_token(self) -> RefreshTokenRepository:
        if self._refresh_token_repo is None:
            self._refresh_token_repo = RefreshTokenRepository(self._session)

        return self._refresh_token_repo

    @property
    def wallet(self) -> WalletRepository:
        if self._wallet_repo is None:
            self._wallet_repo = WalletRepository(self._session)

        return self._wallet_repo

    @property
    def wallet_group(self) -> WalletGroupRepository:
        if self._wallet_group_repo is None:
            self._wallet_group_repo = WalletGroupRepository(self._session)

        return self._wallet_group_repo

    async def __aenter__(self) -> Self:
        self._session = self._session_factory()

        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type is not None:
            await self.rollback()

        await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
