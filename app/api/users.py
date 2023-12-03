from fastapi import APIRouter, Depends
from ..models.request.users import NewUser
from ..middleware import auth

router = APIRouter()

@router.post("/api/register")
async def register_new_user(new_user: NewUser):
    return {"message":"register a new user"}


@router.get("/api/user")
async def get_user(current_user: str= Depends(auth.get_current_user)):
    """
    Get the user for the currently logged in user
    
    """
    return {"message":"return the current user's data"}






