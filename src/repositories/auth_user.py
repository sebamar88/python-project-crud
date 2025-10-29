from src.schemas.auth_user import AuthUserCreateSchema
from src.models.users_models import AuthUserModel
from src.core.database import async_session
from sqlalchemy import select
from src.utils.passwords import hash_password
from typing import Optional


async def create_user(user: AuthUserCreateSchema) -> AuthUserModel:
    async with async_session() as session:
        hashed_pw = hash_password(user.password)
        new_user = AuthUserModel(
            **user.model_dump(exclude={"password"}), password=hashed_pw
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user


async def change_user_role(user_id: int, new_role: str) -> Optional[AuthUserModel]:
    async with async_session() as session:
        query = await session.get(AuthUserModel, user_id)
        if query:
            query.role = new_role
            await session.commit()
            await session.refresh(query)
            return query
        return None


async def change_user_password(user_id: int, new_password: str) -> AuthUserModel | None:
    async with async_session() as session:
        query = await session.get(AuthUserModel, user_id)
        if query:
            query.password = new_password
            await session.commit()
            await session.refresh(query)
            return query
        return None


async def delete_user(user_id: int) -> bool:
    async with async_session() as session:
        user = await session.get(AuthUserModel, user_id)
        if user:
            await session.delete(user)
            await session.commit()
            return True
        return False


async def login_user(email: str) -> AuthUserModel | None:
    async with async_session() as session:
        query = await session.execute(
            select(AuthUserModel).where(AuthUserModel.email == email)
        )
        user = query.scalars().first()
        return user
