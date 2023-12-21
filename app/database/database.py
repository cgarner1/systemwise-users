from sqlalchemy import Column, Integer, DateTime, func, String, MetaData, LargeBinary, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from dotenv import load_dotenv
import os

load_dotenv()

DB_USER =os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", 5432)

USERS_TABLE_NAME = "users"
TOKENS_TABLE_NAME = "tokens"

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind=engine, class_=AsyncSession, expire_on_commit=False)

# schema
Base = declarative_base()

# application logic needs to treat salt/pwd as bytes NOT UTF8 encoded str
class User(Base):
    __tablename__ = USERS_TABLE_NAME
    id = Column("userid", Integer, primary_key=True, index=True)
    username = Column("username", String, index=True)
    email = Column("email", String, index=True)
    password_hash = Column("passwordhash", LargeBinary, nullable = False, index=False)
    salt = Column("salt", LargeBinary, nullable = False, index=False)
    created_at = Column("created",DateTime(timezone=False), server_default=func.now())
    updated_at = Column("updated",DateTime(timezone=False), server_default=func.now(), onupdate=func.now())

    token = relationship('Token', uselist=False, back_populates='user')

class Token(Base):
    __tablename__ = TOKENS_TABLE_NAME
    id = Column("tokenid", Integer, primary_key=True, index=True)
    user_id = Column("userid", Integer, ForeignKey("users.userid"), nullable=False, index=True)
    refresh_token = Column("refreshtoken", String)
    expires_at = Column("refreshexpiresat", DateTime(timezone = False))
    created_at = Column("created",DateTime(timezone=False), server_default=func.now())
    updated_at = Column("updated",DateTime(timezone=False), server_default=func.now(), onupdate=func.now())

    user = relationship('User', uselist=False, back_populates='token')
    
    # there is ONE token per user at any given time
    __table_args__ = (
        UniqueConstraint('userid', name='unique_user_token'),
    )




metadata = MetaData()

# creates the tables if they haven't been created yet, just in case. This runs syncronously.
# eehhhh don't need this? Schema rather static.
# async with engine.begin() as conn:
#     await conn.run_sync(Base.metadata.create_all(bind=engine))

async def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        await db.close()