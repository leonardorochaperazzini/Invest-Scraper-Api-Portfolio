from .Base import Base

from sqlalchemy.ext.declarative import DeclarativeMeta

class ScraperRun(Base):
   def __init__(self, model: DeclarativeMeta) -> None:
      super().__init__(model)
      