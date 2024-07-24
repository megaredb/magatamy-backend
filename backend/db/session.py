from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.utils import config

engine = create_engine(config.DATABASE_CONNECTION)
SessionLocal = sessionmaker(bind=engine)
