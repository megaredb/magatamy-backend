from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from backend.schemas.ticket import answer, form, question
from backend.utils.ticket import TicketStatus


class TicketBase(BaseModel):
    form_id: int


class TicketCreateIn(TicketBase):
    answers: List[answer.AnswerCreate]


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    status: TicketStatus


class TicketInDBBase(TicketBase):
    id: int
    created_at: datetime
    status: TicketStatus
    answers: List[answer.Answer]
    author_id: Optional[str] = None

    class Config:
        from_attributes = True


class Ticket(TicketInDBBase):
    pass


class TicketInDB(TicketInDBBase):
    pass
