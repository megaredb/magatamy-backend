from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.sql import expression

from backend.db.base_class import Base

if TYPE_CHECKING:
    from backend.models import Form


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(1024))
    image: Mapped[str] = mapped_column(String(128))
    operation: Mapped[int] = mapped_column(Integer, nullable=False)
    custom_command: Mapped[str] = mapped_column(String)
    connected_form_id: Mapped[int] = mapped_column(ForeignKey("form.id"))
    connected_form: Mapped["Form"] = relationship()
    popular: Mapped[bool] = mapped_column(Boolean, server_default=expression.true())


class Promo(Base):
    __tablename__ = "promo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String)
    percent: Mapped[float] = mapped_column(Float)
    usages: Mapped[int] = mapped_column(Integer, default=0)
    valid_to = mapped_column(DateTime)
