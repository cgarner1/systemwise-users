import asyncio
from datetime import datetime, timedelta

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from fastapi import HTTPException, status

from database import Token
from middleware.auth_middleware import REFRESH_TOKEN_EXPIRE_DAYS



# note: we have ONE refresh token per user.
async def create_or_update_refresh_token(db : AsyncSession, user_id : int, refresh_token : str, exp : datetime):
    try:
        statement = insert(Token).values(
            user_id = user_id,
            refresh_token = refresh_token,
            expires_at = exp
        ).on_conflict_do_update(
            index_elements=['userid'],
            set_={
                'refreshtoken' : refresh_token,
                'refreshexpiresat' : exp,
                'updated' : exp - timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
            }
        )

        await db.execute(statement)
        await db.commit()

    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to write refresh token to postgresDB"
        )
