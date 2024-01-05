from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import mapped_column, Mapped

from db.base_class import Base


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False, index=True)
    command: Mapped[str] = mapped_column(String, nullable=False, deferred=True)
    description: Mapped[str] = mapped_column(String(1024))
    image: Mapped[str] = mapped_column(String(128))
