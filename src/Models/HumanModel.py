from sqlalchemy import Column, String, Integer, BOOLEAN,ForeignKey

from src.database import Base

class Human(Base):
    __tablename__ = 'human'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer, default=0)
    mother_id = Column(Integer, ForeignKey('human.id',ondelete='SET NULL'), nullable=True)
    pregnancy = Column(Integer, default=None,nullable=True)
    father_id = Column(Integer, ForeignKey('human.id',ondelete='SET NULL'),nullable=True)
    sex = Column(String)
    last_partner = Column(Integer, ForeignKey('human.id',ondelete='SET NULL'), default=None, nullable=True)
    death_or_alive = Column(BOOLEAN)


