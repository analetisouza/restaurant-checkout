import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import select

from models.models import Base, Category, Item

engine = create_engine(
    "postgresql+psycopg2://myuser:mypassword@restaurant-checkout-postgres-1:5432/restaurant_checkout")
Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(bind=engine))

file = open("./data/menu.json")

data = json.load(file)


def app():

    categories = []
    for category in data['categories']:
        categories.append(Category(id=category['id'], name=category['name'], image_id=category['image_id']))

    items = []
    for item in data['items']:
        items.append(Item(id=item['id'], name=item['name'], price=item['price'], image_id=item['image_id'],
                          category_id=item['category_id']))

    with Session() as session:
        session.add_all(categories)
        session.add_all(items)
        session.commit()

    with engine.connect() as conn:
        stmt = select(Category)
        print(conn.execute(stmt).fetchall())
        stmt = select(Item)
        print(conn.execute(stmt).fetchall())


if __name__ == "__main__":
    app()
