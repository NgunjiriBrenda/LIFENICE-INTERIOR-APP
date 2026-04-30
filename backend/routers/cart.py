from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import CartItem, Product, User
from schemas import CartItemCreate, CartItemUpdate, CartItemOut, CartOut
from routers.auth import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/", response_model=CartOut)
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)

):
    items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    total = sum(item.product.price * item.quantity for item in items)
    return CartOut(items=items, total=total, item_count=len(items))



@router.post("/", response_model=CartItem, status_code=201)
def add_to_cart(
    item_data: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(
        Product.id == item_data.product_id,
        Product.is_active == True
    ).first()
    if not product:
       raise HTTPException(status_code=404, detail="Product not found")
    
    if product.stock < item_data.quanity:
        raise HTTPException(
            status_code=400,
            detail=f"Only {product.stock}items in stock"
        )

    existing = db.query(CartItem).filter(
        CartItem.user_id == current_user.id,
        CartItem.product_id == item_data.product_id

    ).first()
    if existing:
        new_qty = existing.quantity + item_data.quantit
        if product.stock < new_qty:
            raise HTTPException(
                status_code=400,
                detail=f"Only {product.stock} items in stock"

            )
        existing.quantity = new_qty
        db.commit()
        db.efresh(existing)
        return existing

    cart_item = CartItem(
        user_id=current_user.id,
        product_id=item_data.product_id,
        quantity=item_data.quantity
    )
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item

@router.patch("/{item_id}", response_model=CartItemOut)
def update_cart_item(
    item_id: int,
    item_data: CartItemUpdate,
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == current_user.id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    if item.product.stock < item_data.quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Only {item.product.stock} in stock"
        )
    
    item.quantity = item_data.quantity
    db.commit()
    db.refresh(item)
    return item
@router.delete("/{item_id}", status_code=204)
def remove_from_cart(
    item_id: int,
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == current_user.id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item  not found")
    
    db.delete(item)
    db.commit()


    
@router.delete("/", status_code=204)
def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)_

):
    db.query(CartItem).filter(CartItem.user_id == current_user)
    db.commit()





   
  