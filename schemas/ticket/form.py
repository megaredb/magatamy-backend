from typing import List
from pydantic import BaseModel
from schemas.ticket import question


class FormBase(BaseModel):
    name: str


class FormCreate(FormBase):
    pass


class FormUpdate(FormBase):
    pass


class FormInDBBase(FormCreate):
    id: int
    questions: List[question.Question]

    class Config:
        from_attributes = True


class Form(FormInDBBase):
    pass


class FormInDB(FormInDBBase):
    pass
