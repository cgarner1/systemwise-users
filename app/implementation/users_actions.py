from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from database.database import User

async def add_user_to_db(db, user):    
    try:
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
    except IntegrityError as e:
        db.rollback()

        # todo -> define if email or usrname
        if "unique constraint" in str(e):
            raise HTTPException(status_code=400, detail="Username or email already registered")

async def get_user_by_id():
    pass

async def get_user_by_username(db : AsyncSession, username : str):
    statement = select(User).where(User.username == username)
    result = await db.execute(statement)
    user = result.fetchone()

    return user[0]

