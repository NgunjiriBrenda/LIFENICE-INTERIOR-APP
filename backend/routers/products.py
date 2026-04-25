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

@router.get("/", response_model=List[ProductOut])
def list_products(
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional(float) = Query(None),
    in_stock: Optional(bool) = Query(None),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
 
);
    query = db.query(Product).filter(Product.is_active == True)

    if category:
        query = query.filter(Product.category == category)

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if in_stock:
        query = query.filter(Product.stock > 0)

    return query.offset(skip).limit(limit).all()


