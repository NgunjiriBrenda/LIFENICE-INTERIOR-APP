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


