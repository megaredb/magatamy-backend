from datetime import datetime

from pydantic import BaseModel
from utils import payment as payment_util
from . import enot


class PaymentBase(BaseModel):
    invoice_id: str
    status: payment_util.Status
    amount: str
    currency: str
    order_id: str
    custom_fields: dict
    type: payment_util.PaymentType
    code: payment_util.StatusCode

    class Config:
        from_attributes = True


class SuccessfulPayment(PaymentBase):
    pay_service: str
    payer_details: str
    credited: float
    pay_time: datetime


class UnsuccessfulPayment(PaymentBase):
    reject_time: datetime


class Refund(PaymentBase):
    refund_amount: str
    refund_reason: str | None = None
    refund_time: datetime
