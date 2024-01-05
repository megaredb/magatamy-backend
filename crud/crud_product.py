from typing import Any

from sqlalchemy.orm import Session, undefer, Query

from crud.base import CRUDBase
from models import Product
from schemas.product import ProductCreate, ProductUpdate


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100, is_admin: bool = False
    ):
        query: Query = db.query(self.model).offset(skip)

        if is_admin:
            query = query.options(undefer(Product.command))

        return query.limit(limit).all()

    def get(self, db: Session, _id: Any, is_admin: bool = False):
        query: Query = db.query(self.model).filter(self.model.id.is_(_id))

        if is_admin:
            query = query.options(undefer(Product.command))

        return query.first()


product = CRUDProduct(Product)
