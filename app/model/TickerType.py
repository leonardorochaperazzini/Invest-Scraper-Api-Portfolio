from sqlalchemy import Column, BigInteger, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

STOCKS_BR_ID = 1
FII_ID = 2

class TickerType(Base):
  __tablename__ = 'tickers_types'
  __table_args__ = {'schema': 'invest'}

  id = Column(BigInteger, primary_key=True)
  name = Column(String)