import enum


class AnswerType(enum.Enum):
    TEXT = 0
    BOOL = 1

    @staticmethod
    def from_value(value: str | bool) -> "AnswerType":
        match type(value):
            case value if value is bool:
                return AnswerType.BOOL
            case _:
                return AnswerType.TEXT


class TicketStatus(enum.Enum):
    OPEN = 0
    CLOSED = 1
