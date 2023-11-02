from crud.base import CRUDBase
from models import Product
from schemas.product import ProductCreate, ProductUpdate


class CRUDDiscordUser(CRUDBase[Product, ProductCreate, ProductUpdate]):
    pass


product = CRUDDiscordUser(Product)
