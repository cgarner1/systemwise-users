import asyncio
from datetime import datetime, timedelta

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from fastapi import HTTPException, status

from database import Token
from middleware.auth_middleware import REFRESH_TOKEN_EXPIRE_DAYS



# note: we have ONE refresh token per user.
def create_or_update_refresh_token(db : Session, user_id : int, refresh_token : str, exp : datetime):
    print(type(exp))
    try:
        statement = insert(Token).values(
            user_id = user_id,
            refresh_token = refresh_token,
            expires_at = exp
        ).on_conflict_do_update(
            index_elements=['userid'],
            set_={
                'refresh_token' : refresh_token,
                'expires_at' : exp,
                'updated_at' : exp - timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
            }
        )

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to write refresh token to DB"
        )
