
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from typing import Optional
from models.request.auth_request import LoginRequest

from middleware import auth_middleware
from database import SessionLocal, engine, Base, User, get_db
from implementation.tokens_actions import create_or_update_refresh_token




auth_router = APIRouter()
@auth_router.post("/api/logout")
async def logout(current_user:str=Depends(auth_middleware.get_current_user_from_jwt)):
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

    # if we have gotten past raise_exception_if_token_exists middleware, user has not passed jwt to this request
        
    # if no auth header, request the salt and pwd hash for a user.
    # Keep in mind, user.salt is bytes, NOT string
    user : User = db.query(User).filter_by(username=login_request.username).first()
    password_attempt_hash, salt = auth_middleware.get_or_create_password_hash(login_request.password, user.salt)

    if password_attempt_hash == user.password_hash:
        jwt = auth_middleware.create_jwt(user.id)
        refresh_token, exp = auth_middleware.create_refresh_token(user.id)
        print(f"outside call:{type(exp)}")
        # we always create a new token on new login, and save a SINGLE token per user.
        # more DB writes, and longer lived tokens, however, securtiy requirements have a less severe impact than most products
        # additionally, there is no case where we need multiple active sessions.
        create_or_update_refresh_token(db, user.id, refresh_token, exp)
        
        return {
            "access_token": jwt,
            "token_type":"bearer",
            "refresh_token": refresh_token
        }
            

    raise HTTPException(status_code=401, detail="authentication failed")
    

# todo -> we need the JWT AND the refresh token
@auth_router.post("/api/refresh-token")
async def refresh_token():

    return {"message":"refresh login token"}