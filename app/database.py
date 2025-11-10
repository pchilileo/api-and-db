from sqlmodel import Session, create_engine, SQLModel
from app.config import database_path

engine = create_engine(database_path)

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
    
def init_db():
    SQLModel.metadata.create_all(engine)
    print("Database initialized.")