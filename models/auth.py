from typing import List, TYPE_CHECKING

from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped, relationship, synonym

from db.base_class import Base
from models.associations import users_to_forms_associations

if TYPE_CHECKING:
    from models import Form


class User(Base):
    __tablename__ = "user"
    discord_id = mapped_column(String(32), primary_key=True, index=True)
    id = synonym("discord_id")
    created_at = mapped_column(DateTime, server_default=func.now())
    last_login = mapped_column(DateTime, server_default=func.now())

    purchased_forms: Mapped[List["Form"]] = relationship(
        secondary=users_to_forms_associations
    )
