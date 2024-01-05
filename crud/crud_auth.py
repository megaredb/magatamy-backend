from typing import Optional, Any

from sqlalchemy.orm import Session

from crud.base import CRUDBase, ModelType
from models import User
from schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_discord_id(self, db: Session, discord_id: Any) -> Optional[User]:
        return (
            db.query(self.model).filter(self.model.discord_id.is_(discord_id)).first()
        )


user = CRUDUser(User)
