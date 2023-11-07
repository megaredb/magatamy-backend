from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import mapped_column

from db.base_class import Base


class Product(Base):
    __tablename__ = "product"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String(64), nullable=False)
    price = mapped_column(Float, nullable=False, index=True)
    command = mapped_column(String, nullable=False)
