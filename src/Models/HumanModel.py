from sqlalchemy import Column, String, Integer

from src.database import Base

class Human(Base):
    __tablename__ = 'human'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer, default=0)
    male = Column(String)
    weight = Column(Integer)
    height = Column(Integer)
