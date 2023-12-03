
from fastapi import APIRouter, Depends
from ..middleware import auth

router = APIRouter()
@router.post("/api/logout")
async def logout(current_user:str=Depends(auth.get_current_user)):
    """
    logs out a user. Think this will just invalidate the current refresh token?
    """
    return {"message":"deleted refresh token. Remove the cookie on users device"}

@router.post("/api/login")
async def login(username:str, password: str):

    return {"message":"logs in a new user"}

# todo -> we need the JWT AND the refresh token
@router.post("/api/refresh-token")
async def login():

    return {"message":"logs in a new user"}