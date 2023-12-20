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
REFRESH_TOKEN_EXPIRE_DAYS = 45


# todo -> only gets username
def get_current_user_from_jwt(token: str=Depends(lambda x: x.header("Authorization"))):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )

    try:
        token = token.split("Bearer ")[1]
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        user_id: int = payload.get("sub")

        if user_id is not None:
            return user_id
        
        raise credentials_exception
        
    except JWTError:
        raise credentials_exception


# todo -> jwt lacks scopes, iss
def create_jwt(user_id : int) -> str:
    payload = {
        "sub":user_id,
        "exp": datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        ),
        "iat":datetime.utcnow()
    }

    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm = 'HS256')

    return token

# todo -> iss after hosting, handle secrets rotation 
def create_refresh_token(user_id : int) -> (str, datetime):
    now = datetime.utcnow()
    payload = {
        "sub":user_id,
        "exp": now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        "iat": now
    }

    # jwt.encode modifies payload. save first, 
    # DO NOT RETURN payload["foo"]after encoding!
    expiry = payload["exp"]
    refresh_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm = 'HS256')
    
    return refresh_token, expiry

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
    