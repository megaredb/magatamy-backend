from typing import Any

from sqlalchemy.orm import Session, undefer, Query

from crud.base import CRUDBase
from models import Product
from schemas.product import ProductCreate, ProductUpdate


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    pass


product = CRUDProduct(Product)
