#В этом файле прописаны исключения приложения

class AppError(Exception):
    """Возникла базовая ошибка в работе приложения"""

class MailAlreadyExist(AppError):
    """Такая почта уже существует"""

class WrongPassword(AppError):
    """Неверный пароль"""

class NoRights(AppError):
    """Нет прав"""

class NotFounded(AppError):
    """Объекта в базе не существует"""

class ServerMistake(AppError):
    """Возникла проблема извне: сервис OpenRouter вернул ошибку"""