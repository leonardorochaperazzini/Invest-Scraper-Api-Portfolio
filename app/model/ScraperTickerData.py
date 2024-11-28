from sqlalchemy import Column, BigInteger, JSON
from .Base import Base

class ScraperTickerData(Base):
  __tablename__ = 'scraper_tickers_data'
 
  scraper_run_ticker_id = Column(BigInteger)
  data = Column(JSON)