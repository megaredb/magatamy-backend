from typing import Optional, Any

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models import User, Form
from schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_discord_id(self, db: Session, discord_id: Any) -> Optional[User]:
        return (
            db.query(self.model).filter(self.model.discord_id.is_(discord_id)).first()
        )

    def add_purchased_form(self, db: Session, user_in: User, form_in: Form) -> User:
        user_in.purchased_forms.append(form_in)

        db.commit()
        db.refresh(user_in)

        return user_in

    def remove_purchased_form(self, db: Session, user_in: User, form_in: Form) -> User:
        user_in.purchased_forms.remove(form_in)

        db.commit()
        db.refresh(user_in)

        return user_in


user = CRUDUser(User)
