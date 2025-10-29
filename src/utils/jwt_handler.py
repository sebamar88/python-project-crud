from datetime import datetime, timedelta
from jose import JWTError, jwt
from src.core.config import settings


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    jwt_secret = settings.JWT_SECRET
    jwt_algorithm = settings.JWT_ALGORITHM
    try:
        encoded_jwt = jwt.encode(to_encode, jwt_secret, algorithm=jwt_algorithm)
    except JWTError:
        return ""
    return encoded_jwt
