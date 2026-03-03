from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://arka:password123@localhost/tokodb")

engine = create_engine(DATABASE_URL)

class Base(DeclarativeBase):
    pass

def get_db():
    with Session(engine) as session:
        yield session
