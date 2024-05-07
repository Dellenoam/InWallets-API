from auth.models import RefreshToken, User
from repository import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(SQLAlchemyRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model_cls=User)


class RefreshTokenRepository(SQLAlchemyRepository[RefreshToken]):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model_cls=RefreshToken)
