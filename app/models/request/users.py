from pydantic import BaseModel

class NewUser(baseModel):
    username: str
    password: str
    email: str