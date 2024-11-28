from sqlalchemy import Column, BigInteger
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

class Base(BaseModel):
  __abstract__ = True
  __tablename__ = None
  __table_args__ = {'schema': 'invest'}

  id = Column(BigInteger, primary_key=True)