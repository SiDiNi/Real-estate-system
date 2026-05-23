from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.core.security import create_jwt_token
from app.crud.crud_user import user_crud
from app.models.models import User
from app.schemas.schemas import TokenResponse, UserCreate, UserLogin, UserResponse


router = APIRouter()


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Регистрация нового пользователя.
    """
    # Проверка, существует ли пользователь
    user = await user_crud.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400, detail="Пользователь с таким именем уже существует"
        )

    user = await user_crud.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400, detail="Пользователь с таким Email уже существует"
        )

    new_user = await user_crud.create(db, obj_in=user_in)
    return new_user


@router.post("/login", response_model=TokenResponse)
async def login(
    user_in: UserLogin,  # Нужно добавить UserLogin в schemas, если нет, или использовать UserCreate
    db: AsyncSession = Depends(get_db),
):
    user = await user_crud.authenticate(
        db, username=user_in.username, password=user_in.password
    )

    if not user:
        raise HTTPException(
            status_code=400, detail="Неверное имя пользователя или пароль"
        )

    # Создаем токен
    token_data = {"sub": user.username}
    access_token = create_jwt_token(token_data)

    return TokenResponse(
        access_token=access_token, token_type="bearer", message="Успешный вход"
    )


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Получить информацию о текущем пользователе.
    """
    return current_user
