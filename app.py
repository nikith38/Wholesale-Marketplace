from fastapi import Depends, FastAPI
from pydantic import BaseModel
from typing import List
from schemas import User, Product, Order, OrderItem,CartItem
from db import get_db,Base,engine
import crud
from sqlalchemy.orm import Session


app=FastAPI()
Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return "Wholesale Marketplace API is running"

@app.post("/auth/register/", response_model=User)
def register_user(user: User,db: Session = Depends(get_db)):
    return crud.register_user(user,db)

@app.get("/users/", response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.post("/auth/login/")
def login_user():
    return {"message": "Login functionality to be implemented"}

@app.post("/add_product/", response_model=Product)
def add_product(product: Product, db: Session = Depends(get_db)):
    return crud.add_product(product, db)

@app.get("/products/", response_model=List[Product])
def get_products(db: Session = Depends(get_db)):    
    return crud.get_products(db)

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return crud.get_product(product_id, db)

@app.post("/add_to_cart/", response_model=CartItem)
def add_to_cart(cart_item: CartItem, db: Session = Depends(get_db)):
    return crud.add_to_cart(cart_item, db)

@app.get("/cart/{buyer_id}")
def get_cart(buyer_id: int, db: Session = Depends(get_db)):
    return crud.get_cart(buyer_id, db)

@app.get("/orders/calculate_discount/")
def calculate_discount(buyer_id: int,db: Session = Depends(get_db)):
    return crud.calculate_discount(buyer_id,db)

@app.post("/place_order/")
def place_order(buyer_id: int, db: Session = Depends(get_db)):
    return crud.place_order(buyer_id, db)

@app.post("/clear_cart/{buyer_id}")
def clear_cart(buyer_id: int, db: Session = Depends(get_db)):
    return crud.delete_cart(buyer_id, db)

@app.get("/orders/{buyer_id}")
def get_orders(buyer_id: int, db: Session = Depends(get_db)):
    return crud.get_orders(buyer_id, db)