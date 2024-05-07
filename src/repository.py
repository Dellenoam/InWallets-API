from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Sequence, TypeVar

from database import Base
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType", bound=Base)


class AbstractRepository(ABC, Generic[ModelType]):
    @abstractmethod
    async def create(self, data: Dict[str, Any]) -> ModelType:
        raise NotImplementedError

    @abstractmethod
    async def create_multiple(self, data: Dict[str, Any]) -> Sequence[ModelType]:
        raise NotImplementedError

    @abstractmethod
    async def get_by(self, **filters: Any) -> ModelType | None:
        raise NotImplementedError

    @abstractmethod
    async def get_multiple_by(self, **filters: Any) -> Sequence[ModelType]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, obj_to_update: ModelType, data: Dict[str, Any]) -> ModelType:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, obj_to_delete: ModelType) -> None:
        raise NotImplementedError


class SQLAlchemyRepository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model_cls: type[ModelType]) -> None:
        self._session = session
        self._model_cls = model_cls

    async def create(self, data: Dict[str, Any]) -> ModelType:
        new_obj = self._model_cls(**data)
        self._session.add(new_obj)
        await self._session.flush()

        return new_obj

    async def create_multiple(
        self, data: Sequence[Dict[str, Any]]
    ) -> Sequence[ModelType]:
        new_objs = [self._model_cls(**datum) for datum in data]
        self._session.add_all(new_objs)
        await self._session.flush()

        return new_objs

    async def get_by(self, **filters: Any) -> ModelType | None:
        statement = select(self._model_cls).filter_by(**filters)
        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def get_multiple_by(self, **filters: Any) -> Sequence[ModelType]:
        statement = select(self._model_cls).filter_by(**filters)
        result = await self._session.execute(statement)

        return result.scalars().all()

    async def update(self, obj_to_update: ModelType, data: Dict[str, Any]) -> ModelType:
        for key, value in data.items():
            setattr(obj_to_update, key, value)

        await self._session.flush()

        return obj_to_update

    async def delete(self, obj_to_delete: ModelType) -> None:
        await self._session.delete(obj_to_delete)
