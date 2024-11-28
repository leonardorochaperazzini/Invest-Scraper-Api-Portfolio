from sqlalchemy import Column, Boolean, BigInteger, String, TIMESTAMP
from .Base import Base

class ScraperRunTicker(Base):
  __tablename__ = 'scraper_runs_tickers'
 
  scraper_run_id = Column(BigInteger)
  ticker_id = Column(BigInteger)
  started_at = Column(TIMESTAMP)
  ended_at = Column(TIMESTAMP)
  exec_failed = Column(Boolean)
  cause_exec_failed = Column(String)