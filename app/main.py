from fastapi import FastAPI
from api import users_router, auth_router


app = FastAPI()

# include routers
app.include_router(users_router, prefix="/api/v1", tags=["users"])
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])


@app.get("/keepalive")
async def root():
    return {"message": "OK"}
