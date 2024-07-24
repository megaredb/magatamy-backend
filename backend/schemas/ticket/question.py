from pydantic import BaseModel

from backend.utils.ticket import AnswerType


class QuestionBase(BaseModel):
    form_id: int
    position: int
    title: str
    description: str
    answer_type: AnswerType


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(QuestionBase):
    pass


class QuestionInDBBase(QuestionCreate):
    id: int

    class Config:
        from_attributes = True


class Question(QuestionInDBBase):
    pass


class QuestionInDB(QuestionInDBBase):
    pass
