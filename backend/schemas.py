from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    phone_number: Optonal[str] = None

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
            return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    phone_number: Optional[str]
    is_admin: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class TokenData(BaseModel):
    user_id: Optional[int] = None

class ProductCreate(BaseModel):
    name: str
    category: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    stock: int = 0

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Price must be greater than 0")

        return v

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] =  None
    price: Optional[float] = None
    image_url: Optional[str] = None
    stock: Optional[int] = None
    is_active: Optional[bool] = None


class ProductOut(BaseModel):
    id: int
    name: str
    category: str
    description: Optional[str]
    price: float
    image_url: Optional[str]
    stock: int
    is_active: bool
    created_at: datetime

class Config:
    product_id: int
    quantity: int = 1

    @field_validator("quantity")
    @classmethod
    @classmethod
    def quantity_must_be_positive(cls, v):
        if v < 1:
            raise ValueError("Quantity must be at least 1")

        return v

class CartItemUpdate(BaseModel):
    quantity: int

class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: ProductOut

    class Config:
        from_attributes = True

class CartOut(BaseModel):
    items: List[CartItemOut]
    total: float
    item_count: int


class OrderItemOut(BaseModel):
    id: int
    product_id: Optional[int]
    quantity: int
    price: float
    product: Optional[ProductOut]

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    delivery_address: str
    phone_number: str
    notes: Optional[str] = None

class OrderOut(BaseModel):
    id: int
    user_id: Optional[int]
    total_amout: float
    status: str
    payment_reference: Optional[str]
    delivery_address: Optional[str]
    created_at: datetime
    order_items: List[OrderItemOut]

    class config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: str


class MpesaSTKPushRequest(BaseModel):
    order_id: int
    phone_number: str

class PaymentResponse(BaseModel):
    success: bool
    message: str
    checkout_request_id: Optional[str] = None
    order_id: Optional[int] = None














