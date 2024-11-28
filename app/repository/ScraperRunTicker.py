from .Base import Base

from sqlalchemy.ext.declarative import DeclarativeMeta

class ScraperRunTicker(Base):
   def __init__(self, model: DeclarativeMeta) -> None:
      super().__init__(model)
      