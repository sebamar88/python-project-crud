from src.repositories.auth_user import (
    create_user,
    change_user_role,
    change_user_password,
    delete_user,
    login_user,
)
from src.utils.passwords import verify_password, hash_password, needs_rehash
from src.schemas.auth_user import AuthUserCreateSchema, AuthUserBaseSchema
from src.utils.jwt_handler import create_access_token
from fastapi import HTTPException, status
from datetime import timedelta

ACCESS_TOKEN_EXPIRE_MINUTES = 10


async def login(email: str, password: str):
    user = await get_user_by_email(email)
    if not user or not verify_password(password, user.password):
        return None

    # Si el hash es viejo → actualizar
    if needs_rehash(user.password):
        new_hash = hash_password(password)
        await change_user_password(user.id, new_hash)

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

    # 👇 no lo hashees acá, pasalo plano
    user_data = AuthUserCreateSchema(email=email, password=password, role=role)
    new_user = await create_user(user_data)
    return AuthUserBaseSchema.model_validate(new_user)


async def update_user_role(user_id: int, new_role: str) -> AuthUserBaseSchema:
    updated_user = await change_user_role(user_id, new_role)
    return AuthUserBaseSchema.model_validate(updated_user)


async def update_user_password(user_id: int, new_password: str) -> AuthUserBaseSchema:
    updated_user = await change_user_password(user_id, new_password)
    return AuthUserBaseSchema.model_validate(updated_user)


async def remove_user(user_id: int) -> bool:
    result = await delete_user(user_id)
    return result


async def get_user_by_email(email: str):
    user = await login_user(email)
    return user
