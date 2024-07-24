from typing import List, Type

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.models import Ticket
from backend.schemas.ticket import TicketCreate, TicketUpdate


class CRUDTicket(CRUDBase[Ticket, TicketCreate, TicketUpdate]):
    def create_with_author(
        self, db: Session, *, obj_in: TicketCreate, author_id: int
    ) -> Ticket:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, author_id=author_id)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def get_multi_by_author(
        self, db: Session, *, author_id: int, skip: int = 0, limit: int = 100
    ) -> List[Type[Ticket]]:
        return (
            db.query(self.model)
            .filter(Ticket.author_id == author_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


ticket = CRUDTicket(Ticket)
