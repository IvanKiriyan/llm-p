from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import User

class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session #хранит как приватное поле

    async def get_user_email(self, email: str) -> User | None: #получение пользователя по email
        result = await self._session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_user_id(self, user_id: int) -> User | None: #получение пользователя по айди
        result = await self._session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def create(self, email:str, password_hash: str, #создание пользователя, который добавляет Orm-объект в сессию
                     role: str = "user") -> User:
        user = User(email=email, password_hash=password_hash, role=role)
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user