from app.core.errors import MailAlreadyExist, NotFounded, WrongPassword
from app.core.security import token_acess_password, secure_password, check_password
from app.db.models import User
from app.repositories.users import UserRepository

class UsecaseAuth: #бизнес-логика регистрации и логина
    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo
    
    async def registration(self, email: str, password: str) -> User:
        existing = await self._user_repo.get_user_email(email)
        if existing:
            raise MailAlreadyExist(f"Email {email} уже существует")
        secured = secure_password(password)
        return await self._user_repo.create(email=email, password_hash=secured)
    
    async def login(self, email: str, password: str) -> str:
        user = await self._user_repo.get_user_email(email)
        if not user or not check_password(password, user.password_hash):
            raise WrongPassword("Неверная почта или пароль")
        return token_acess_password(user_id=user.id, role=user.role)
    
    async def get_profile(self, user_id: int) -> User:
        user = await self._user_repo.get_user_id(user_id)
        if not user:
            raise NotFounded(f"Такой пользователь {user_id} не найден")
        return user