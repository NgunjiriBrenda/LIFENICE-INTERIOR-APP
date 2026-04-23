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

