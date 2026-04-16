from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def secure_password(password: str) -> str: #хэширование пароля через passlib
    return pwd_context.hash(password)

def check_password(plain: str, hashed: str) -> bool: #проверка пароля
    return pwd_context.verify(plain, hashed)