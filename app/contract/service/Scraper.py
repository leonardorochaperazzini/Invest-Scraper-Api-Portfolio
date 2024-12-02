from abc import ABC, abstractmethod

from pydantic import BaseModel

class Scraper(ABC):
    @abstractmethod
    def call_url(self, url: str):
        pass

    @abstractmethod
    def get_data(self, ticker: str) -> BaseModel:
        pass
    
    @abstractmethod
    def get_data_from_ticker(self, ticker: str) -> BaseModel:
        pass

 