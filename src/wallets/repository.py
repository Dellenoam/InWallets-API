from typing import Any, Dict, List, Sequence

from sqlalchemy import delete, select

from repository import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession
from wallets.models import Wallet, WalletGroup


class WalletRepository(SQLAlchemyRepository[Wallet]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model_cls=Wallet)

    async def filter_by_wallet_ids(self, wallet_ids: List[int]) -> Sequence[Wallet]:
        statement = select(self._model_cls).filter(self._model_cls.id.in_(wallet_ids))
        result = await self._session.execute(statement)

        return result.scalars().all()

    async def update_multiple_wallets(
        self, wallets_to_patch: Sequence[Wallet], wallet_mappings: List[Dict[str, Any]]
    ) -> Sequence[Wallet]:
        for wallet_to_patch, wallet_mapping in zip(wallets_to_patch, wallet_mappings):
            for key, value in wallet_mapping.items():
                setattr(wallet_to_patch, key, value)
        
        await self._session.flush()

        return wallets_to_patch

    async def delete_multiple_wallets(
        self, wallet_ids: List[int], user_id: int
    ) -> None:
        statement = delete(self._model_cls).where(self._model_cls.id.in_(wallet_ids))

        await self._session.execute(statement)


class WalletGroupRepository(SQLAlchemyRepository[WalletGroup]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model_cls=WalletGroup)
