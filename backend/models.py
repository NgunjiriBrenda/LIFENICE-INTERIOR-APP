from sqlalchemy import (
    Column, Integer, String, Float, Boolean, ForeignKey,DateTime, Text

)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
form database import Base
import enum


class User(Base):
    __tablename__="users"

    id = Column(Interger, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    cart_items = relationship("CartItem", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user")
  
