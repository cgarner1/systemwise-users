import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import bcrypt

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = 15


# todo -> only gets username
def get_current_user(token: str=Depends(lambda x: x.header("Authorization"))):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )

    try:
        token = token.split("Bearer ")[1]
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        username:str = payload.get("sub")

        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception


# todo -> jwt lacks roles
def create_jwt(username:str) -> str:
    payload = {
        "sub":username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    }

    token = jwt.decode(payload, JWT_SECRET_KEY, algorithms=JWT_SECRET_KEY)

    return token

def get_password_hash(password:str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password, salt