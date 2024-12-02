from abc import ABC, abstractmethod

class Base(ABC):
    @abstractmethod
    def all(self, limit: int, offset: int, filter: object) -> list:
        pass
    
    @abstractmethod
    def create(self, data: object) -> object:
        pass
    
    @abstractmethod
    def update(self, id: int, data: object) -> object:
        pass
    
    @abstractmethod
    def get_current_date(self) -> str:
        pass
