from src.repositories.auth_user import (
    create_user,
    change_user_role,
    change_user_password,
    delete_user,
    login_user,
)
from src.utils.passwords import verify_password, hash_password
from src.schemas.auth_user import AuthUserCreateSchema, AuthUserBaseSchema
from datetime import timedelta
from src.utils.jwt_handler import create_access_token
from fastapi import HTTPException, status

ACCESS_TOKEN_EXPIRE_MINUTES = 10


async def login(email: str, password: str):
    user = await get_user_by_email(email)
    if not user or not verify_password(password, user.password):
        return None

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


async def authenticate_user(email: str, password: str) -> bool:
    user = await login_user(email)
    if not user:
        return False
    return verify_password(password, user.password)


async def register_user(
    email: str, password: str, role: str = "user"
) -> AuthUserBaseSchema:
    existing = await get_user_by_email(email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    hashed_password = hash_password(password)
    user_data = AuthUserCreateSchema(email=email, password=hashed_password, role=role)
    new_user = await create_user(user_data)
    return AuthUserBaseSchema.from_orm(new_user)


async def update_user_role(user_id: int, new_role: str) -> AuthUserBaseSchema:
    updated_user = await change_user_role(user_id, new_role)
    return AuthUserBaseSchema.from_orm(updated_user)


async def update_user_password(user_id: int, new_password: str) -> AuthUserBaseSchema:
    updated_user = await change_user_password(user_id, new_password)
    return AuthUserBaseSchema.from_orm(updated_user)


async def remove_user(user_id: int) -> bool:
    result = await delete_user(user_id)
    return result


async def get_user_by_email(email: str):
    user = await login_user(email)
    return user
