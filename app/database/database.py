from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from ..config import settings
SQL_ALCHEMY_URL = f'postgresql://{settings.DATABASE_NAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}/ecommerceApi'

engine = create_engine(SQL_ALCHEMY_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db(): 
    db = SessionLocal()
    try: 
        yield db 
    finally: 
        db.close()


