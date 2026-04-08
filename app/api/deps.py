from sqlalchemy.orm import Session, sessionmaker
from app.core.database import db

def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()