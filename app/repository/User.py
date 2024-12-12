from .Base import Base

from sqlalchemy.ext.declarative import DeclarativeMeta

class User(Base):
   def __init__(self, model: DeclarativeMeta) -> None:
      super().__init__(model)
      