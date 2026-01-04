from fastapi import APIRouter, HTTPException, status, Depends
# from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db.session import get_session
from app.models.users import User, Role
from app.schemas.user import UserCreate, UserRead
from app.core.security import get_password_hash


router = APIRouter()

@router.post("/register", response_model=UserRead)
async def register_user(
        user_in: UserCreate,
        session: AsyncSession = Depends(get_session)
):
    """
        Регистрирует пользователя, назначая ему по умолчанию роль "user"

        Args:
            user_in (UserCreate): Пользователь, которого нужно зарегистрировать
            session (AsyncSession): Сессия БД

        Returns:
            UserRead: Зарегистрированный пользователь
    """

    # Проверка на существование пользователя с таким же email
    query = (select(User).where(User.email == user_in.email))
    result = await session.execute(query)

    if result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже зарегистрирован!"
        )

    # Назначаем пользователю роль "user"
    role_id = user_in.role_id
    if role_id is None:
        query_role = (select(Role).where(Role.name == "user"))
        result_role = await session.execute(query_role)
        role_obj = result_role.scalar_one_or_none()

        if role_obj is None:
            role_obj = Role(name="user")
            session.add(role_obj)
            await session.commit()
            await session.refresh(role_obj)

        role_id = role_obj.id

    # Создаем нового пользователя, формируем его объект и добавляем в БД
    new_user = User(
        email=str(user_in.email),
        hashed_password=get_password_hash(user_in.password),
        name=user_in.name,
        surname=user_in.surname,
        last_name=user_in.last_name,
        role_id=role_id,
        is_active=True
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user