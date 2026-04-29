from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel): #pydantic-схемы для регистрации
    email: EmailStr
    password: str = Field(min_lenght=8, max_lenght=64)

class TokenResponse(EmailStr):
    access_token: str
    token_type: str = "bearer"