from sqlalchemy import create_engine, Column, Integer, Date, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Cycle(Base):
    __tablename__ = 'cycles'
    name = Column(String, nullable=False)
    id = Column(Integer, primary_key=True)
    start_date = Column(Date, nullable=False)

    def __repr__(self):
        return f"Cycle(id={self.id}, start_date={self.start_date}, name={self.name})"

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
