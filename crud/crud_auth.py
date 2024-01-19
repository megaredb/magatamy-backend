from typing import Optional, Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models import User, Form
from schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_discord_id(self, db: Session, discord_id: Any) -> Optional[User]:
        stmt = select(self.model).where(User.discord_id == discord_id)  # type: ignore

        return db.execute(stmt).scalar()

    @staticmethod
    def add_purchased_form(db: Session, user_in: User, form_in: Form) -> User:
        user_in.purchased_forms.append(form_in)

        db.commit()
        db.refresh(user_in)

        return user_in

    @staticmethod
    def remove_purchased_form(db: Session, user_in: User, form_in: Form) -> User:
        user_in.purchased_forms.remove(form_in)

        db.commit()
        db.refresh(user_in)

        return user_in


user = CRUDUser(User)
