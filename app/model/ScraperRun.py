from sqlalchemy import Column, BigInteger, TIMESTAMP
from .Base import Base

class ScraperRun(Base):
  __tablename__ = 'scraper_runs'

  started_at = Column(TIMESTAMP)
  ended_at = Column(TIMESTAMP)