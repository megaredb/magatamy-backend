from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.models import Product, Promo
from backend.schemas.product import ProductCreate, ProductUpdate
from backend.schemas.product.promo import PromoCreate, PromoUpdate


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    pass


class CRUDPromo(CRUDBase[Promo, PromoCreate, PromoUpdate]):
    def get_by_name(self, db: Session, name: str) -> Optional[Promo]:
        stmt = select(self.model).where(self.model.name == name)

        return db.execute(stmt).scalar()


product = CRUDProduct(Product)
promo = CRUDPromo(Promo)
