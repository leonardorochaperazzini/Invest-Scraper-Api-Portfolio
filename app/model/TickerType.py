from sqlalchemy import Column, BigInteger, String
from .Base import Base

STOCKS_BR_ID = 1
FII_ID = 2

class TickerType(Base):
  __tablename__ = 'tickers_types'
 
  name = Column(String)