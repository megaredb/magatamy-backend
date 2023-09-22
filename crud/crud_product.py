from crud.base import CRUDBase
from models import Product
from schemas.product import ProductCreate, ProductUpdate


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    pass


product = CRUDProduct(Product)
