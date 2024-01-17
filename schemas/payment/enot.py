from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class InvoiceCreateResponseData(BaseModel):
    id: str
    amount: int
    currency: str
    url: str
    expired: datetime


class InvoiceCreateResponse(BaseModel):
    data: Optional[InvoiceCreateResponseData] = None
    error: Optional[str] = None
    status: int
    status_check: bool

    class Config:
        from_attributes = True
