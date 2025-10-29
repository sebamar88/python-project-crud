from datetime import datetime, timedelta
from jose import jwt
from src.core.config import settings


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Crea un JWT con los datos del usuario y un tiempo de expiración.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt
