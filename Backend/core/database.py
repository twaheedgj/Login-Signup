from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(settings.get_database_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    SQLModel.metadata.create_all(engine) 

def get_session():
    with Session(engine) as session:
        yield session