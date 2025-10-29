from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from src.core.config import settings
from src.services.auth_user import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Verifica el token JWT y devuelve el usuario autenticado.
    Si el token no es válido o está expirado, lanza un 401.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_by_email(email)
    if user is None:
        raise credentials_exception

    return user
