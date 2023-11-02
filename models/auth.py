from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import mapped_column

from db.base_class import Base


class User(Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True, index=True)
    discord_id = mapped_column(String(32))
    registration_date = mapped_column(DateTime, server_default=)
