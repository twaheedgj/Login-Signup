from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from core.config import Config
import uuid
import logging
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def generate_token(user_dict: dict, expires_delta: timedelta=None, refresh: bool=False) -> str:
    payload = {}
    payload['user_id'] = user_dict
    payload['exp'] = datetime.now() + (expires_delta if expires_delta else timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES))
    payload['iat'] = datetime.now()
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh
    encoded_jwt = jwt.encode(payload,
                              Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)
    return encoded_jwt

def decode_tokken(token:str)->dict:
    try:
        jwt.decode(token, 
                   Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
    except jwt.PyJWTError as e:
        logging.exception(f"Error decoding token: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
