from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_auth_usecase, get_current_user_id
from app.core.errors import MailAlreadyExist, NotFounded, WrongPassword
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import UsecaseAuth

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserPublic, #эндпоинт регистрации
             status_code=status.HTTP_201_CREATED)
async def register(
    body: RegisterRequest,
    usecase: UsecaseAuth = Depends(get_auth_usecase),
):
    try:
        return await usecase.registration(email=body.email, 
                                          password=body.password)
    except MailAlreadyExist as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=str(e))

@router.post("/login", response_model=TokenResponse) #эндпоинт логина
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    usecase: UsecaseAuth = Depends(get_auth_usecase),
):
    try:
        token = await usecase.login(email=form.username, 
                                    password=form.password)
        return TokenResponse(access_token=token)
    except WrongPassword as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authentificate": "Bearer"},
        )

@router.get("/me", response_model=UserPublic) #эндпоинт профиля
async def get_me(
    user_id: int = Depends(get_current_user_id),
    usecase: UsecaseAuth = Depends(get_auth_usecase),
):
    try:
        return await usecase.get_profile(user_id)
    except NotFounded as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=str(e))