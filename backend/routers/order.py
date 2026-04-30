from fastapi import APIRouter, Depends, HTTPException, status
from  sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Order, OrderItem, CartItem, Product, User
from schemas import OrderCreate, OrderOut, OrderStatusUpdate
from routers.auth import get_current_user, get_admin_user

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderOut, status_code=201)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)


):
     cart_items = db.query(CartItem).filter(
          CartItem.user_id == current_user.id
     ).all()

     if not cart_items:
          raise HTTPException(
               status_code=400
               detail = "Your cart is empty"
          )
     
     for item in cart_items:
          if item.product.stock < item.quantity:
               raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for '{item.product.name}'. Available: {item.product.stock}"
               )
     total = sum(item.product.price * item.quantity for item in cart_items)

     order = Order(
          user_id=current_user.id,
          total_amount=total,
          status="pending",
          delivery_address=order_data.delivery_address,
     ) 
     db.add(order)
     db.flush()

     for item in cart_items:
          order_item = OrderItem(
               order_id= Order.id,
               product_id=item.product_id,
               quantity=item.quantity,
               price=item.product.price
          ) 
          db.add(order_item)
          item.product.stock -= item.quantity

     db.query(CartItem).filter(
         CartItem.user_id == current_user.id

      ).delete()

     db.commit()
     db.refresh(order)
     return order

@router.get("/my-orders", response_model=List[OrderOut])
def get_my_orders(
     db: Session = Depends(get_db),
     current_user: User = Depends(get_current_user)   
):
     return db.query(Order).filter(
          Order.user_id == current_user.id

     ).order_by(Order.created_at.desc()).all()
     



