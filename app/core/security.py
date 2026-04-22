from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def secure_password(password: str) -> str: #хэширование пароля через passlib
    return pwd_context.hash(password)

def check_password(plain: str, hashed: str) -> bool: #проверка пароля
    return pwd_context.verify(plain, hashed)

def token_acess_password(user_id: int, role: str) -> str: #генерация токена
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "role": role,
        "iat": now,
        "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)

def decode_password_token (token: str) -> dict: #функция декодинга токена
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])