import enum
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Integer, DateTime, func, ForeignKey, String, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship
from db.base_class import Base


class Form(Base):
    __tablename__ = "form"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    questions: Mapped[List["Question"]] = relationship(back_populates="form")


class AnswerType(enum.Enum):
    TEXT = "text"
    BOOL = "bool"


class Question(Base):
    __tablename__ = "question"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    form_id: Mapped[int] = mapped_column(ForeignKey("form.id"))
    form: Mapped["Form"] = relationship(back_populates="questions")
    answer_type: Mapped[AnswerType]


class Answer(Base):
    __tablename__ = "answer"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"))
    question: Mapped["Question"] = relationship()
    ticket_id: Mapped[int] = mapped_column(ForeignKey("ticket.id"))
    value: Mapped["AnswerValue"] = relationship(back_populates="answer")


class AnswerValue(Base):
    __tablename__ = "answer_value"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    answer_id: Mapped[int] = mapped_column(ForeignKey("answer.id"))
    answer: Mapped["Answer"] = relationship(back_populates="value")
    text_value: Mapped[Optional[str]] = mapped_column(String(4096))
    bool_value: Mapped[Optional[bool]] = mapped_column(Boolean)


class TicketStatus(enum.Enum):
    OPEN = "open"
    CLOSED = "closed"


class Ticket(Base):
    __tablename__ = "ticket"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author = relationship("User")
    form_id: Mapped[int] = mapped_column(ForeignKey("form.id"))
    form: Mapped["Form"] = relationship()
    answers: Mapped[List["Answer"]] = relationship()
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    status: Mapped[TicketStatus]
