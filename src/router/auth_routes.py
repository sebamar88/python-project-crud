from fastapi import APIRouter, HTTPException, status
from src.services.auth_user import (
    register_user,
    login as login_user,
)
from src.schemas.auth_user import (
    AuthUserCreateSchema,
    AuthUserLoginSchema,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(user: AuthUserCreateSchema):
    new_user = await register_user(
        email=user.email, password=user.password, role=user.role or "user"
    )
    return {"user": new_user}


@router.post("/login")
async def login(user: AuthUserLoginSchema):
    token = await login_user(email=user.email, password=user.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return token
