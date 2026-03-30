from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    time_spent_alone = Column(Float)
    social_event_attendance = Column(Float)
    going_outside = Column(Float)
    friends_circle_size = Column(Float)
    post_frequency = Column(Float)
    stage_fear = Column(String)
    drained_after_socializing = Column(String)
    prediction = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class APIKey(Base):
      __tablename__ = "api_keys"

      id = Column(Integer, primary_key=True, index=True)
      key = Column(String, unique=True, index=True)
      owner = Column(String)
      is_active = Column(String, default="true")
      
def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()