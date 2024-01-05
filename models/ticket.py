from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Integer, DateTime, func, ForeignKey, String, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.base_class import Base
from utils.ticket import TicketStatus

if TYPE_CHECKING:
    from .auth import User
else:
    User = "User"


class Form(Base):
    __tablename__ = "form"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(64))
    questions: Mapped[List["Question"]] = relationship(back_populates="form")


class Question(Base):
    __tablename__ = "question"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    position: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(String(4096))
    form_id: Mapped[int] = mapped_column(ForeignKey("form.id"))
    form: Mapped["Form"] = relationship(back_populates="questions")
    answer_type: Mapped[int] = mapped_column(Integer, default=0)


class Answer(Base):
    __tablename__ = "answer"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"))
    question: Mapped["Question"] = relationship()
    ticket_id: Mapped[int] = mapped_column(ForeignKey("ticket.id"))
    ticket: Mapped["Ticket"] = relationship(back_populates="answers")
    text_value: Mapped[Optional[str]] = mapped_column(String(4096))
    bool_value: Mapped[Optional[bool]] = mapped_column(Boolean)


class Ticket(Base):
    __tablename__ = "ticket"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship()
    form_id: Mapped[int] = mapped_column(ForeignKey("form.id"))
    form: Mapped["Form"] = relationship()
    answers: Mapped[List["Answer"]] = relationship(back_populates="ticket")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    status: Mapped[int] = mapped_column(
        Integer, default=TicketStatus.OPEN.value, nullable=False
    )
