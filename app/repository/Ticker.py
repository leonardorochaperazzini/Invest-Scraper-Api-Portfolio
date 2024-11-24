from .Base import Base

class Ticker(Base):
   def __init__(self, model):
      super().__init__(model)

   def get_names_list(self, limit = 10, offset = 0, filter = None):
      tickers = self.all(limit, offset, filter)
      return [ticker.name for ticker in tickers]
      
      