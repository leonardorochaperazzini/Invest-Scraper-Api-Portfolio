from sqlalchemy import Column, BigInteger, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ScraperRun(Base):
  __tablename__ = 'scraper_runs'
  __table_args__ = {'schema': 'invest'}

  id = Column(BigInteger, primary_key=True)
  started_at = Column(TIMESTAMP)
  ended_at = Column(TIMESTAMP)