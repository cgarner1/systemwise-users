from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext

import bcrypt

from models.request.users_request import RegisterUserRequest
from middleware import auth_middleware
from database import SessionLocal, engine, Base, User, get_db
from implementation import users_actions

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

users_router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@users_router.post("/users/register")
async def register_new_user(register_user_request: RegisterUserRequest, db: Session = Depends(get_db)):
    
    hashed_password, new_salt = auth_middleware.get_or_create_password_hash(register_user_request.password)
    
    # salt/pwd are saved as bytes datatype. Do not do any encoding/decoing here.
    user = User(
        username = register_user_request.username,
        email= register_user_request.email,
        password_hash= hashed_password,
        salt= new_salt
    )
    
    try:
        db_user = users_actions.add_user_to_db(db, user)
        return {db_user.username, db_user.email, db_user.created_at}
    
    except IntegrityError as e:
        db.rollback()

        if "unique constraint" in str(e):
            raise HTTPException(status_code=400, detail="Username or email already registered")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@users_router.get("users")
async def get_user(current_user: str= Depends(auth_middleware.get_current_user_from_jwt)):
    """
    Get the user for the currently logged in user
    
    """
    return {"message":"return the current user's data"}






