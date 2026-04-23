from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import optional
import os
from dotenv import load_dotenv

from database import get_db
from model import User
from schemas import UserRegister, UserLogin, UserOut, Token, TokenData

load_dotenv()

router = APIRouter(prefix="/auth", tags=["Aunthentication"])
 
SECRET_KEY = os.getenv("SECRET_KEY", "lifeNIceinteriors-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str ) -> bool:
    return pwd_password_context.verify(plain_password, hashed_password)

def create access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
