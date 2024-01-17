from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.base_class import Base

if TYPE_CHECKING:
    from models import Form


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(1024))
    image: Mapped[str] = mapped_column(String(128))
    operation: Mapped[int] = mapped_column(Integer, nullable=False)
    connected_form_id: Mapped[int] = mapped_column(ForeignKey("form.id"))
    connected_form: Mapped["Form"] = relationship()
