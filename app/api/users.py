from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext

import bcrypt

from models.request.users import RegisterUserRequest
from middleware import auth

from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base, User

users_router = APIRouter()

# oauth2_Scheme = OAuth2PasswordBearer(tokenUrl="token") todo : move to auth
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@users_router.post("/users/register")
async def register_new_user(register_user_request: RegisterUserRequest, db: Session = Depends(get_db)):
    hashed_password, new_salt = auth.get_password_hash(register_user_request.password)
    user = User(
        username = register_user_request.username,
        email= register_user_request.email,
        password_hash= hashed_password,
        salt= new_salt
    )

    db.Add(user)
    db.commit()
    db.refresh(user)
    
    return user


@users_router.get("users")
async def get_user(current_user: str= Depends(auth.get_current_user)):
    """
    Get the user for the currently logged in user
    
    """
    return {"message":"return the current user's data"}






