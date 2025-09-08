from db import SessionLocal
from schemas import User, Product, Order, OrderItem,CartItem
from sqlalchemy.orm import Session
from datetime import datetime
from models import User as DBUser
from models import Product as DBProduct
from models import CartItem as DBCartItem
from models import Order as DBOrder

def register_user(user: User, db: Session):
    db_user = DBUser(
        id=user.id,
        username=user.username,
        email=user.email,
        user_type=user.user_type,
        company_name=user.company_name,
        created_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(DBUser).all()

def add_product(product: Product, db: Session):
    db_product = DBProduct(
        id=product.id,
        vendor_id=product.vendor_id,
        name=product.name,
        category=product.category,
        price=product.price,
        min_quantity=product.min_quantity,
        stock=product.stock,
        created_at=datetime.utcnow()
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session):
    return db.query(DBProduct).all()

def get_product(product_id: int, db: Session):
    return db.query(DBProduct).filter(DBProduct.id == product_id).first()

def add_to_cart(cart_item: CartItem, db: Session):
    db_cart_item = DBCartItem(
        id=cart_item.id,
        buyer_id=cart_item.buyer_id,
        product_id=cart_item.product_id,
        quantity=cart_item.quantity,
        added_at=datetime.utcnow()
    )
    db.add(db_cart_item)
    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item

def get_cart(buyer_id: int, db: Session):
    my_cart=db.query(DBCartItem).filter(DBCartItem.buyer_id == buyer_id).all()
    #fetch product details for each cart item
    items=[]
    for item in my_cart:
        product=db.query(DBProduct).filter(DBProduct.id==item.product_id).first()
        item.product_name=product.name
        item.unit_price=product.price
        item.subtotal=product.price*item.quantity
        items.append(item)
    return items

def calculate_discount(buyer_id: int,db: Session):
    """
    Discount Rules:
    1. Quantity Bonus: 100+ units = 5%, 500+ units = 10%, 1000+ units = 15%
    2. Value Bonus: $1000+ = 3%, $5000+ = 7%, $10000+ = 12%
    3. Loyalty Bonus: Previous orders count (1-3 orders = 2%, 4+ orders = 5%)

    Maximum discount: 25%
    """
    # Fetch cart items for the buyer
    my_cart=db.query(DBCartItem).filter(DBCartItem.buyer_id == buyer_id).all()
    if not my_cart:
        return {"message": "Cart is empty"}
    total_quantity = sum(item.quantity for item in my_cart)
    total_value = sum(db.query(DBProduct).filter(DBProduct.id==item.product_id).first().price * item.quantity for item in my_cart)
    previous_orders_count = db.query(DBOrder).filter(DBOrder.buyer_id == buyer_id).count()
    discount_percent = 0
    # Quantity Bonus
    if total_quantity >= 1000:
        discount_percent += 15
    elif total_quantity >= 500:
        discount_percent += 10
    elif total_quantity >= 100:
        discount_percent += 5
    # Value Bonus
    if total_value >= 10000:
        discount_percent += 12
    elif total_value >= 5000:
        discount_percent += 7
    elif total_value >= 1000:
        discount_percent += 3
    #Loyalty Bonus
    if previous_orders_count >= 4:
        discount_percent += 5
    elif previous_orders_count >= 1:
        discount_percent += 2
    # Calculate the maximum discount
    if discount_percent > 25:
        discount_percent = 25

    return {"discount": f"{discount_percent}%", "total_quantity": total_quantity, "total_value": total_value, "previous_orders": previous_orders_count,"new_total": total_value * (1 - discount_percent / 100)}


def delete_cart(buyer_id: int, db: Session):
    my_cart=db.query(DBCartItem).filter(DBCartItem.buyer_id == buyer_id).all()
    for item in my_cart:
        db.delete(item)
    db.commit()
    return {"message": "Cart cleared"}


def place_order(buyer_id: int, db: Session):
    data=calculate_discount(buyer_id,db)
    my_cart=db.query(DBCartItem).filter(DBCartItem.buyer_id == buyer_id).all()
    if not my_cart:
        return {"message": "Cart is empty"}
    Order_total = data['total_value']
    discount_percent = int(data['discount'].strip('%'))
    final_amount = data['new_total']
    db_order = DBOrder(
        buyer_id=buyer_id,
        total_amount=Order_total,
        discount_percent=discount_percent,
        final_amount=final_amount,
        created_at=datetime.utcnow()
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    # Clear the cart after placing the order
    delete_cart(buyer_id, db)
    #reduce stock
    for item in my_cart:
        product=db.query(DBProduct).filter(DBProduct.id==item.product_id).first()
        product.stock-=item.quantity
        db.add(product)
        db.commit()
        db.refresh(product)
    return db_order

def get_orders(buyer_id: int, db: Session):
    return db.query(DBOrder).filter(DBOrder.buyer_id == buyer_id).all()

