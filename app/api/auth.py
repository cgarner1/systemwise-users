
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from typing import Optional
from models.request.auth_request import LoginRequest

from middleware import auth_middleware
from database import SessionLocal, engine, Base, User, get_db



auth_router = APIRouter()
@auth_router.post("/api/logout")
async def logout(current_user:str=Depends(auth_middleware.get_current_user)):
    """
    logs out a user. Think this will just invalidate the current refresh token?
    """
    return {"message":"deleted refresh token. Remove the cookie on users device"}

@auth_router.post("/login")
async def login(
    login_request: LoginRequest,
    token: str = Depends(auth_middleware.raise_exception_if_token_exists),
    db: Session = Depends(get_db)
    ):

    # if we have gotten past raise_exception_if_token_exists middleware, user has not passed jwt o this request
        
    # if no auth header, request the salt and pwd hash for a user.
    # Keep in mind, user.salt is bytes, NOT string
    user = db.query(User).filter_by(username=login_request.username).first()
    password_attempt_hash, salt = auth_middleware.get_or_create_password_hash(login_request.password, user.salt)

    if password_attempt_hash == user.password_hash:
        jwt = auth_middleware.create_jwt(login_request.username)
        

        return {"access_token": jwt, "token_type":"bearer"}

    raise HTTPException(status_code=401, detail="authentication failed")
    

# todo -> we need the JWT AND the refresh token
@auth_router.post("/api/refresh-token")
async def login():

    return {"message":"logs in a new user"}