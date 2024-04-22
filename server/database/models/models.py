from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())
    image_id: Mapped[str] = mapped_column(String())

    def __repr__(self) -> str:
        return f"Category(id={self.id!r}, name={self.name!r}, image_id={self.image_id!r})"


class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())
    image_id: Mapped[str] = mapped_column(String())
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    price: Mapped[float] = mapped_column()

    def __repr__(self) -> str:
        return f"Item(id={self.id!r}, name={self.name!r}, image_id={self.image_id!r}, \
        category_id={self.category_id!r}, price={self.price!r})"


class CartItem(Base):
    __tablename__ = "cart_item"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey('item.id'))
    quantity: Mapped[int] = mapped_column()
    cart_id: Mapped[int] = mapped_column(ForeignKey("cart.id"))

    def __repr__(self) -> str:
        return f"CartItem(id={self.id!r}, item_id={self.item_id!r}, quantity={self.quantity!r}, \
        cart_id={self.cart_id!r})"


class Cart(Base):
    __tablename__ = "cart"

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_items: Mapped[List["CartItem"]] = relationship()

    def __repr__(self) -> str:
        return f"Cart(id={self.id!r}, cart_items={self.cart_items!r})"


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("cart.id"))
    payment_id: Mapped[int] = mapped_column(ForeignKey("payment.id"))
    status: Mapped[str] = mapped_column(String())
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=func.now())

    def __repr__(self) -> str:
        return f"Order(id={self.id!r}, cart_id={self.cart_id!r}, payment_id={self.payment_id!r}, \
        status={self.status!r}, created_at={self.created_at!r})"


class Payment(Base):
    __tablename__ = "payment"

    id: Mapped[int] = mapped_column(primary_key=True)
    card_type: Mapped[str] = mapped_column(String())
    card_number: Mapped[int] = mapped_column()
    expiration_month: Mapped[int] = mapped_column()
    expiration_year: Mapped[int] = mapped_column()
    security_code: Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return f"Payment(id={self.id!r}, card_type={self.card_type!r}, card_number={self.card_number!r}, \
        expiration_month={self.expiration_month!r}, expiration_year={self.expiration_year!r}, \
        security_code={self.security_code!r})"
