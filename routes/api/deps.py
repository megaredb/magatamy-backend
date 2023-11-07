from typing import Generator, Any
from sqlalchemy.orm import Session
from db.session import SessionLocal


def get_db() -> Generator[Session, Any, None]:
    database = SessionLocal()

    try:
        yield database
    finally:
        database.close()
