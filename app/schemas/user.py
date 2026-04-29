from pydantic import BaseModel, EmailStr

class UserPublic(BaseModel): #описана публичная схема пользователя
    model_config = {"from_attributes": True}

    id: str
    email: EmailStr
    role: str