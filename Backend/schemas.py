# schemas.py
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str | None = None

class UserInDB(UserResponse):
    hashed_password: str