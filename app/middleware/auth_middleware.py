import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status, Request, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
import bcrypt


load_dotenv()
oauth_password_scheme = oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
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
        "exp": datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    }

    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm = 'HS256')

    return token

def get_or_create_password_hash(password:str, salt: bytes = None):
    salt = bcrypt.gensalt() if salt is None else salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password, salt



async def raise_exception_if_token_exists(authorization: str = Header(None)):
    """
    returns 400 to user if an auth token is passed in. Returns None if no header exists
    """
    
    if authorization and authorization.startswith('Bearer '):
        raise HTTPException(status_code=400, detail="Already Authenticated")
    return authorization if authorization else None
    