from configs.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine(settings.db.URL)

async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
