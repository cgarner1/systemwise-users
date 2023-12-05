from fastapi import FastAPI
from database import SessionLocal, engine, Base, User

app = FastAPI()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"messge": "helloworld"}
