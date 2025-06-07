from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import URL
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = 'postgresql+psycopg2://postgres:postgres@localhost:5432/sims'

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/sims')

session_maker = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)

class Base(DeclarativeBase):
    pass