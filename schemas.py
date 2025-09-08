import datetime
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class User(BaseModel):
    id: int
    username: str
    email: str
    user_type: Literal["VENDOR", "BUYER"]
    company_name: str
    #created_at: str

class Product(BaseModel):
    id: int
    vendor_id: int
    name: str
    category: str
    price: float 
    min_quantity: int
    stock: int
    #created_at: str

class Order(BaseModel):
    id: int
    buyer_id: int
    total_amount: float
    discount_percent: float
    final_amount: float
    created_at: str


class OrderItem(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: float
    subtotal: float


class CartItem(BaseModel):
    id: int
    buyer_id: int
    product_id: int
    quantity: int
    #added_at: str