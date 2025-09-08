from sqlalchemy import  Column, Integer, String,Enum,Float
from db import Base
import datetime
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    user_type = Column(Enum("VENDOR", "BUYER"), index=True)
    company_name = Column(String, index=True)
    created_at = Column(String, default=datetime.datetime.utcnow)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, index=True) #foreign_key="users.id"
    name = Column(String, index=True)
    category = Column(String, index=True)
    price = Column(Float)
    min_quantity = Column(Integer)
    stock = Column(Integer)
    created_at = Column(String, default=datetime.datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, index=True)#foreign_key="users.id"
    total_amount = Column(Float)
    discount_percent = Column(Float)
    final_amount = Column(Float)
    created_at = Column(String, default=datetime.datetime.utcnow)

class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, index=True)
    product_id = Column(Integer, index=True)
    quantity = Column(Integer)
    added_at = Column(String, default=datetime.datetime.utcnow)

