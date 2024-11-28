from .Base import Base

from sqlalchemy.ext.declarative import DeclarativeMeta

class Ticker(Base):
   def __init__(self, model: DeclarativeMeta) -> None:
      super().__init__(model)

   def get_names_list(self, limit: int = 10, offset: int = 0, filter: object = None) -> list[str]:
      tickers = self.all(limit, offset, filter)
      return [ticker.name for ticker in tickers]
      
      