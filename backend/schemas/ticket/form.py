from typing import List, Optional

from pydantic import BaseModel

from backend.schemas.ticket import question


class FormBase(BaseModel):
    name: str
    purchasable: bool = False
    extra_id: str


class FormCreate(FormBase):
    pass


class FormUpdate(FormBase):
    name: Optional[str] = None
    purchasable: Optional[bool] = None
    extra_id: Optional[str] = None


class FormInDBBase(FormCreate):
    id: int
    questions: List[question.Question]

    class Config:
        from_attributes = True


class Form(FormInDBBase):
    has_access: Optional[bool] = True


class FormInDB(FormInDBBase):
    pass
