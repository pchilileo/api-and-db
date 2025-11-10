from sqlmodel import Session, create_engine, SQLModel
from app.config import database_path

engine = create_engine(database_path)
SQLModel.metadata.create_all(engine)

def get_session():
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()