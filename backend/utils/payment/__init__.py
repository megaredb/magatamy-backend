import enum


class Status(enum.StrEnum):
    """
    SUCCESS = "success"
    EXPIRED = "expired"
    REFUND = "refund"
    """

    SUCCESS = "success"
    EXPIRED = "expired"
    REFUND = "refund"


class StatusCode(enum.IntEnum):
    """
    SUCCESS = 1
    SUCCESSFUL_REFUND = 20
    EXPIRED = 31
    INVOICE_CLOSED = 32
    """

    SUCCESS = 1
    SUCCESSFUL_REFUND = 20
    EXPIRED = 31
    INVOICE_CLOSED = 32


class PaymentType(enum.IntEnum):
    """
    PURCHASE = 1
    REFUND = 2
    """

    PURCHASE = 1
    REFUND = 2
