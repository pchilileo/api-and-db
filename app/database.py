from sqlmodel import Session, create_engine, SQLModel

from app.config import settings
import app.models.user
import app.models.task

engine = create_engine(settings.database_path)

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

def add_commit_refresh(session: Session, instance):
    session.add(instance)
    session.commit()
    session.refresh(instance)
    return instance

init_db()