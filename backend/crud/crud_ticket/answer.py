from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.models import Answer
from backend.schemas.ticket.answer import AnswerUpdate, AnswerCreate


class CRUDAnswer(CRUDBase[Answer, AnswerCreate, AnswerUpdate]):
    def create_with_ticket(
        self, db: Session, *, obj_in: AnswerCreate, ticket_id: int
    ) -> Answer:
        obj_in_data: dict = jsonable_encoder(obj_in)

        db_obj = self.model(**obj_in_data, ticket_id=ticket_id)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj


answer = CRUDAnswer(Answer)
