from fastapi import APIRouter, Depends

from models.request.users import RegisterUserRequest
from middleware import auth

from sqlalchemy.orm import Session

users_router = APIRouter()
from database import SessionLocal, engine, Base, User


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@users_router.post("/users/register")
async def register_new_user(new_user: RegisterUserRequest, db: Session = Depends(get_db)):
    
    user = User(
        username = RegisterUserRequest.username,
        email=RegisterUserRequest.email,
        password_hash=RegisterUserRequest.password # todo -> hash and salt
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






