from sqlalchemy import Column, BigInteger, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Ticker(Base):
  __tablename__ = 'tickers'
  __table_args__ = {'schema': 'invest'}

  id = Column(BigInteger, primary_key=True)
  name = Column(String)
  ticker_type_id = Column(BigInteger)