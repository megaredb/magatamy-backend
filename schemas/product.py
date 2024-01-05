from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str
    image: Optional[str] = None
    price: float


class ProductCreate(ProductBase):
    command: str


class ProductUpdate(ProductCreate):
    name: Optional[str] = None
    price: Optional[float] = None
    command: Optional[str] = None


class ProductInDBBase(ProductBase):
    id: int

    class Config:
        from_attributes = True


class Product(ProductInDBBase):
    command: Optional[str] = None


class ProductInDB(ProductInDBBase):
    command: str
