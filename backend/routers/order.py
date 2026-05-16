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
               status_code=400,
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

@router.get("/{order_id}", response_model=OrderOut)
def get_order(
     order_id: int,
     db: Session = Depends(get_db),
     current_user: User = Depends(get_current_user)
):
     order = db.query(Order).filter(
          Order.id == order_id,
          Order.user_id == current_user.id
     ).first()
     if not order:
        raise HTTPException(status_code=404, detail="Order not found")
     return order
       
     

@router.delete("/{order_id}/cancel")
def cancel_order(
     order_id: int,
     db:Session = Depends(get_db),       
     current_user: User = Depends(get_current_user)
    
):  
     order = db.query(Order).filter(
          Order.id == order_id,
          Order.user_id == current_user.id

    ).first()
     if not order:
       raise HTTPException(status_code=404, detail="Order not found")
     if order.status != "pending":
        raise HTTPException(status_code=400, detail="Only pending orders can be canceled")

     for item in order.order_items:
         if item.product:
             item.product.stock += item.qunatity

     order.status = "cancelled"
     db.commit()

     return {"message": "Order cancelled successfully"}


@router.get("/admin/all", response_model=List[OrderOut])
def admin_get_all_orders(
     db: Session = Depends(get_db),
     _: User = Depends(get_admin_user)

):
     return db.query(Order).order_by(Order.created_at.desc()).all()

@router.patch("/admin/{order_id}/status", response_model=OrderOut)
def admin_update_order_status(
     order_id: int,
     status_update: OrderStatusUpdate,
     db: Session = Depends(get_db),
     _: User = Depends(get_admin_user)
 ):
     valid_statuses = [
          "pending", "paid", "processing",
          "shipped", "deliver", "cancelled"
     ]
     if status_data.status not in valid_statuses:
           raise HTTPException(
               status_code=400,
               detail=f"Invalid status.Choose from: {valid_statuses}"

           )
     order = db.query(Order).filter(Order.id == order_id).first()
     if not order:
          raise HTTPException(status_code=404, detail="Order not found")
     
     order.status = status_data.status
     db.commit()
     db.refresh(order)
     return order






