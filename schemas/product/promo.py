from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PromoBase(BaseModel):
    name: str
    percent: float
    valid_to: datetime


class PromoCreate(PromoBase):
    pass


class PromoUpdate(PromoBase):
    name: Optional[str] = None
    percent: Optional[float] = None
    valid_to: Optional[datetime] = None


class PromoInDBBase(PromoBase):
    id: int
    usages: int

    class Config:
        from_attributes = True


class Promo(PromoInDBBase):
    pass
