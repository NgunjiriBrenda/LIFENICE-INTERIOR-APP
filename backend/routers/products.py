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
    max_price: Optional[float] = Query(None),
    in_stock: Optional[bool] = Query(None),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
 
)
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


@router.get("/categories")
def list_categories(db: Session = Depends(get_db)):
    results = (
        db.query(Product.category, func.count(Product.id).label("count"))
        .filter(Product.is_active == True)
        .group_by(Product.category)
        .all()
    )
    return [{"name": row.category, "product_count": row.count} for row in results]

@router.get("/{product_id}", response_model=ProductOut)
def get_products(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.is_active == True
    ).first()
    if not product:
        rause HTTPException(status_code=404, detail="Product not found")

    return product

@admin_router.post("/products", response_model=ProductOut, status_code=201)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user)
):

    product = Product(**product_data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@admin_router.put("/products/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user)
    
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product

@admin_router.delete("/products/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.is_active=False
    db.commit()

@admin_router.get("/products", response_model=List[ProductOut])
def admin_list_all_products(
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user)
):
    return db.query(Product).all()

@admin_router.patch("/products/{product_id}/restock")
def restock_product(
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user)

):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.stock+= quantity
    db.commit()
    return {"message": f"Stock updated. New stock: {product.stock}"}






