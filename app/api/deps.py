from typing import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_password_token
from app.db.session import AsyncSessionLocal
from app.repositories.chat_messages import ChatMessageRepository
from app.repositories.users import UserRepository
from app.services.openrouter_client import ClientOpenRouter
from app.usecases.auth import UsecaseAuth
from app.usecases.chat import UsecaseChat

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_session() -> AsyncGenerator[AsyncSession, None]: #создает сессию бд
    async with AsyncSessionLocal() as session:
        yield session

def get_user_repo(session: AsyncSession = 
                  Depends(get_session)) -> UserRepository: #репозиторий пользователей
    return UserRepository(session)

def get_chat_repo(session: AsyncSession = 
                  Depends(get_session)) -> ChatMessageRepository: #репозиторий сообщений
    return ChatMessageRepository(session)

def get_llm_client() -> ClientOpenRouter: #создает клиент
    return ClientOpenRouter()

def get_auth_usecase(repo: UserRepository = 
                     Depends(get_user_repo)) -> UsecaseAuth: #usecase авторизации
    return UsecaseAuth(repo)

def get_chat_usecase(
        chat_repo: ChatMessageRepository = Depends(get_chat_repo), #usecase чата
        llm: ClientOpenRouter = Depends(get_llm_client),
) -> UsecaseChat:
    return UsecaseChat(chat_repo, llm)

async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int: #логика получения пользователя по jwt
    try:
        payload = decode_password_token(token)
        return int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            details="Неверный токен или истек срок действия",
            headers={"WWW-Authenticate": "Bearer"},
        )