from typing import Optional

from pydantic import BaseModel


class AnswerBase(BaseModel):
    question_id: int
    text_value: Optional[str] = None
    bool_value: Optional[bool] = None


class AnswerCreate(AnswerBase):
    pass


class AnswerUpdate(AnswerBase):
    pass


class AnswerInDBBase(AnswerCreate):
    id: int
    ticket_id: int

    class Config:
        from_attributes = True


class Answer(AnswerInDBBase):
    pass


class AnswerInDB(AnswerInDBBase):
    pass
