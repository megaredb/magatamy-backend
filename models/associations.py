from sqlalchemy import Table, Column, ForeignKey

from db.base_class import Base

users_to_forms_associations = Table(
    "users_to_forms_associations",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("form_id", ForeignKey("form.id"), primary_key=True),
)
