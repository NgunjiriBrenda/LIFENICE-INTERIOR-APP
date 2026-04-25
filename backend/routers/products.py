from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from database import get_db
from models import Product, User
from schemas import ProductCreate, ProductUpdate, ProductOut, AdminDashboardStats
from routers.auth import get_current_user, get_admin_user

router = APIRouter(prefix="/products", tags=["Products"])
admin_router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])

