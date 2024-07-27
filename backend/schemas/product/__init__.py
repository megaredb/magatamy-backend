from typing import Optional

from pydantic import BaseModel

from backend.utils.product import ProductOperation


class ProductBase(BaseModel):
    name: str
    description: str
    image: Optional[str] = None
    price: float
    connected_form_id: Optional[int] = None
    popular: bool
    custom_command: Optional[str] = None


class ProductCreate(ProductBase):
    operation: ProductOperation


class ProductUpdate(ProductCreate):
    name: Optional[str] = None
    price: Optional[float] = None
    operation: Optional[ProductOperation] = None
    description: Optional[str] = None


class ProductInDBBase(ProductBase):
    id: int

    class Config:
        from_attributes = True


class Product(ProductInDBBase):
    operation: Optional[ProductOperation] = None


class ProductInDB(ProductInDBBase):
    operation: ProductOperation
