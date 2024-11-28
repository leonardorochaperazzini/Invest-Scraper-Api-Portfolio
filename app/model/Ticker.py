from sqlalchemy import Column, BigInteger, String
from .Base import Base

class Ticker(Base):
  __tablename__ = 'tickers'
 
  name = Column(String)
  ticker_type_id = Column(BigInteger)