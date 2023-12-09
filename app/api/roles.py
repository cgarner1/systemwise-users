from fastapi import APIRouter, Depends
from ..middleware import auth_middleware

router = APIRouter()

# we need to authorize via user roles!!
@router.post("/api/roles")
async def assign_role(userId:int, role:str, current_user: str= Depends(auth_middleware.get_current_user)):

    return {"message":"assigns a role to a user"}

# todo -> need to authorize by having user roles too
@router.delete("/api/roles")
async def remove_role(userId:int, role:str):
    return {"message":"removes a user role"}