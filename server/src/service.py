from datetime import datetime

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.sql import select, update, delete, and_

from src.common.utils import db_utils
from database.models.models import Category, Item, CartItem, Cart, Payment, Order


class PaymentModel(BaseModel):
    card_type: str
    card_number: int
    expiration_month: int
    expiration_year: int
    security_code: int


class OrderModel(BaseModel):
    cart_id: int
    payment_id: int
    status: str


app = FastAPI()


@app.get("/")
def home():
    return {"message": "Connected to server successfully"}


origins = ["http://localhost:5173", ]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"],
                   allow_credentials=True, expose_headers=["*"])

engine, session = db_utils.connect_to_db()


@app.get("/categories/")
def get_categories(request: Request):
    print(request.headers)
    result = session.query(Category).all()
    return [row.to_dict() for row in result]


@app.get("/items/")
def get_items(category_filter: str):
    if category_filter == "All":
        result = session.query(Item).all()
    else:
        result = session.query(Item).join(Category).filter(Category.name == category_filter)
    return [row.to_dict() for row in result]


@app.post("/cart/")
def create_cart():
    new_cart = Cart()
    session.add(new_cart)
    session.commit()
    return new_cart.id


@app.get("/cart/{cart_id}/")
def get_cart(cart_id: int):
    result = (session.query(CartItem.quantity, Item.id.label("item_id"), Item.name.label("item_name"),
                            Item.image_id, Item.price, Category.name.label("category_name"))
              .filter(CartItem.cart_id == cart_id)
              .join(Item, CartItem.item_id == Item.id).join(Category, Item.category_id == Category.id)
              .order_by(CartItem.id)
              .all())
    return [row._asdict() for row in result]


@app.put("/cart/{cart_id}/")
def update_cart_item(item_id: int, operation: str, cart_id: int):
    with engine.connect() as conn:
        stmt = select(CartItem).filter(and_(CartItem.cart_id == cart_id, CartItem.item_id == item_id))
        result = conn.execute(stmt).fetchone()

        if not result:
            new_cart_item = CartItem(item_id=item_id, quantity=1, cart_id=cart_id)
            session.add(new_cart_item)
            session.commit()
        else:
            if operation == "add":
                session.query(CartItem).filter(and_(CartItem.cart_id == cart_id, CartItem.item_id == item_id)
                                               ).update({"quantity": CartItem.quantity + 1})
                session.commit()
            elif operation == "remove" and result.quantity > 1:
                session.query(CartItem).filter(and_(CartItem.cart_id == cart_id, CartItem.item_id == item_id)
                                               ).update({"quantity": CartItem.quantity - 1})
                session.commit()
            else:
                delete_cart_item(item_id=item_id, cart_id=cart_id)


@app.delete("/cart/{cart_id}/")
def delete_cart_item(cart_id: int, item_id: int):
    session.query(CartItem).filter(and_(CartItem.cart_id == cart_id, CartItem.item_id == item_id)).delete()
    session.commit()


@app.post("/payment/")
def create_payment(card_type: str, card_number: str, expiration_month: str, expiration_year: str, security_code: str):
    new_payment = Payment(card_type=card_type, card_number=card_number,
                          expiration_month=expiration_month, expiration_year=expiration_year,
                          security_code=security_code)
    session.add(new_payment)
    session.commit()
    return new_payment.id


@app.post("/order/")
def create_order(order: OrderModel):
    new_order = Order(cart_id=order.cart_id, payment_id=order.payment_id, status=order.status,
                      created_at=datetime.now())
    session.add(new_order)
    session.commit()
    return new_order.id


if __name__ == "__main__":
    uvicorn.run("src.service:app", host="0.0.0.0", port=8000, reload=True)
