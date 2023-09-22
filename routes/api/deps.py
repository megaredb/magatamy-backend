from typing import Generator

from db.session import SessionLocal


def get_db() -> Generator:
    database: SessionLocal

    try:
        database = SessionLocal()
        yield database
    finally:
        database.close()
