from sqlalchemy import Column, Boolean, BigInteger, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ScrapperRunTicker(Base):
  __tablename__ = 'scrapper_runs_tickers'
  __table_args__ = {'schema': 'invest'}

  id = Column(BigInteger, primary_key=True)
  scrapper_run_id = Column(BigInteger)
  ticker_id = Column(BigInteger)
  started_at = Column(TIMESTAMP)
  ended_at = Column(TIMESTAMP)
  exec_failed = Column(Boolean)
  cause_exec_failed = Column(String)