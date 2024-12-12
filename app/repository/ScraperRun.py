import os
from .Base import Base
from sqlalchemy import and_, func
from sqlalchemy.sql.functions import concat
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.ext.declarative import DeclarativeMeta

class ScraperRun(Base):
   def __init__(self, model: DeclarativeMeta) -> None:
      super().__init__(model)

   def get_scrapers_running(self) -> list:
      self.session.query(self.model).all()
   
      scraper_runs = self.session.query(self.model).filter(
         and_(
            self.model.ended_at == None,
            self.model.started_at >= func.now() - func.cast(concat(os.getenv('SELENIUM_HUB_TIMEOUT'), ' SECONDS'), INTERVAL)
         )
      ).all()

      return scraper_runs

