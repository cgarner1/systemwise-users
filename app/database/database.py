from sqlalchemy import create_engine, Column, Integer, DateTime, func, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os

load_dotenv()

DB_USER =os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", 5432)

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind=engine)

# schema
Base= declarative_base()

class User(Base):
    __tablename__ = "public.users"
    id = Column("userid", Integer, primary_key=True, index=True)
    username = Column("username", String, index=True)
    email = Column("email", String, index=True)
    password_hash = Column("passwordhash", String, index=False)
    salt = Column("salt", String, index=False)
    created_at = Column("created",DateTime(timezone=True), server_default=func.now())
    updated_at = Column("updated",DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

metadata = MetaData()

# creates the tables if they haven't been created yet, just in case
Base.metadata.create_all(bind=engine)