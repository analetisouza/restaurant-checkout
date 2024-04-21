import uvicorn
from fastapi import FastAPI
from sqlalchemy.sql import select, delete, and_

from common.utils import db_utils
from database.models.models import Category, Item, CartItem, Cart

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
    cart = Cart()
    session.add(cart)
    return cart.id


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
        else:
            result.update(quantity=quantity)


@app.delete("/cart/{cart_id}")
def delete_cart_item(cart_id: int, item_id: int):
    with engine.connect() as conn:
        stmt = delete(CartItem).filter(and_(CartItem.cart_id == cart_id, CartItem.item_id == item_id))
        conn.execute(stmt)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
