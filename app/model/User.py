from sqlalchemy import Column, Boolean, String
from .Base import Base

class User(Base):
  __tablename__ = 'users'
 
  username = Column(String)
  full_name = Column(String)
  email = Column(String)
  hashed_password = Column(String)
  disabled = Column(Boolean)