from datetime import datetime, timedelta, timezone
from typing import Dict

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from app.core.config import config
from app.core.exceptions import CustomException


oAuth2p_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET = config.api.secret_key
LIVE_TIME_TOKEN_MINUTES = config.api.live_time_token
ALGORITHM = config.api.algorithm

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_hash_password(password: str) -> str:
    if len(password.encode("utf-8")) > 72:
        password = password.encode("utf-8")[:72].decode("utf-8", errors="ignore")

    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt_token(data: Dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=LIVE_TIME_TOKEN_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)


def get_user_from_token(token: str = Depends(oAuth2p_scheme)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise CustomException(
            status_code=401,
            detail="Время жизни истекло",
            message="Время жизни токена истекло!",
        )
    except jwt.InvalidTokenError:
        raise CustomException(
            status_code=401,
            detail="Неверный токен",
            message="Токен, который вы ввели не верный!",
        )
