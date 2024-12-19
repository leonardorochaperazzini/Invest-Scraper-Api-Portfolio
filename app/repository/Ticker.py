from .Base import Base

from sqlalchemy.ext.declarative import DeclarativeMeta

class Ticker(Base):
   def __init__(self, model: DeclarativeMeta) -> None:
      super().__init__(model)
      
      