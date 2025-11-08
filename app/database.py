from sqlmodel import Session, create_engine, SQLModel
from app.config import database_path

engine = create_engine(database_path)
SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session