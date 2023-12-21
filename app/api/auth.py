
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Optional
from models.request.auth_request import LoginRequest

from middleware import auth_middleware
from database import SessionLocal, engine, Base, User, get_db
from implementation.tokens_actions import create_or_update_refresh_token
from implementation.users_actions import get_user_by_username




auth_router = APIRouter()
@auth_router.post("/api/logout")
async def logout(current_user:str=Depends(auth_middleware.get_current_user_from_jwt)):
    """
    logs out a user. This will just invalidate the current refresh token, and clear client tokens (refresh included)
    """
    return {"message":"deleted refresh token. Remove the cookie on users device"}

@auth_router.post("/login")
async def login(
    login_request: LoginRequest,
    token: str = Depends(auth_middleware.raise_exception_if_token_exists),
    db: AsyncSession = Depends(get_db)
    ):

    # if we have gotten past raise_exception_if_token_exists middleware, user has not passed jwt to this request
        
    # if no auth header, request the salt and pwd hash for a user.
    # Keep in mind, user.salt is bytes, NOT string
    
    user : User = await get_user_by_username(db, login_request.username)
    if not user: raise HTTPException(status_code=400, detail="username not recognized.")
    
    
    password_attempt_hash, salt = auth_middleware.get_or_create_password_hash(login_request.password, user.salt)

    if password_attempt_hash == user.password_hash:
        jwt = auth_middleware.create_jwt(user.id)
        refresh_token, exp = auth_middleware.create_refresh_token(user.id)
        # we always create a new token on new login, and save a SINGLE token per user.
        # more DB writes, and longer lived tokens, however, securtiy requirements have a less severe impact than most products
        # additionally, there is no case where we need multiple active sessions.
        await create_or_update_refresh_token(db, user.id, refresh_token, exp)
        
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