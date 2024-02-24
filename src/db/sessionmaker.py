from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import Configuration

engine = create_engine(Configuration.DB_URI, echo=Configuration.DB_ECHO)
Session = sessionmaker(bind=engine)
