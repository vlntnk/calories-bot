from sqlalchemy import (create_engine, Column, Integer, String, ARRAY, Date, 
                        Text, ForeignKey, Float)
from sqlalchemy.orm import sessionmaker, Session, declarative_base
import logging

from configs.config import DATABASE_URI
from configs.dependency_injection import container

Base = declarative_base()

class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False, unique=True)
    chat_id = Column(String(30), nullable=False, unique=True)
    calories = Column(Integer)
    proteins = Column(Integer)
    fats = Column(Integer)
    carbohydrates = Column(Integer)
    dates = Column(ARRAY(Date))
    consumed = Column(ARRAY(Integer))

class Dishes(Base):
    __tablename__ = 'Dishes'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    dish = Column(Text, nullable=False)
    calories = Column(Integer, nullable=False)
    proteins = Column(Integer)
    fats = Column(Integer)
    carbohydrates = Column(Integer)
    author = Column(String, ForeignKey('Users.username'))

engine = create_engine(DATABASE_URI, echo=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=Session)

container.register("db_session", SessionLocal())

logging.basicConfig(level=logging.DEBUG)


def get_session():
    session = container.get("db_session")()
    try:        
        yield session
    except Exception as e:
        logging.debug(f'{e}')
    finally:
        session.close()

