from datetime import datetime

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.sql import select, delete, and_

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
engine, session = db_utils.connect_to_db()


@app.get("/categories")
def get_categories():
    stmt = select(Category)
    return db_utils.fetch_all_from_db(engine, stmt)


@app.get("/items")
def get_items(category_filter: str):
    if category_filter == "all":
        stmt = select(Item)
    else:
        stmt = (select(Item).select_from(Item).join(Category, Item.category_id == Category.id)
                .where(Category.name == category_filter))
    return db_utils.fetch_all_from_db(engine, stmt)


@app.post("/cart")
def create_cart():
    new_cart = Cart()
    session.add(new_cart)
    session.commit()
    return new_cart.id


@app.get("cart/")
def get_cart(cart_id: int):
    return db_utils.fetch_one_by_id(engine, Cart, cart_id)


@app.put("/cart/{cart_id}")
def update_cart_item(item_id: int, quantity: int, cart_id: int):
    with engine.connect() as conn:
        stmt = select(CartItem).filter(and_(CartItem.cart_id == cart_id, CartItem.item_id == item_id))
        result = conn.execute(stmt).fetchone()

        if len(result) == 0:
            new_cart_item = CartItem(item_id=item_id, quantity=quantity, cart_id=cart_id)
            session.add(new_cart_item)
            session.commit()
        else:
            result.update(quantity=quantity)


@app.delete("/cart/{cart_id}")
def delete_cart_item(cart_id: int, item_id: int):
    with engine.connect() as conn:
        stmt = delete(CartItem).filter(and_(CartItem.cart_id == cart_id, CartItem.item_id == item_id))
        conn.execute(stmt)


@app.post("/payment")
def create_payment(payment: PaymentModel):
    new_payment = Payment(card_type=payment.card_type, card_number=payment.card_number,
                      expiration_month=payment.expiration_month, expiration_year=payment.expiration_year,
                      security_code=payment.security_code)
    session.add(new_payment)
    session.commit()
    return new_payment.id


@app.post("/order")
def create_order(order: OrderModel):
    new_order = Order(cart_id=order.cart_id, payment_id=order.payment_id, status=order.status,
                      created_at=datetime.now())
    session.add(new_order)
    session.commit()
    return new_order.id


if __name__ == "__main__":
    uvicorn.run("src.service:app", host="0.0.0.0", port=8000, reload=True)
