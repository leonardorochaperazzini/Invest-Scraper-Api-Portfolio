from .ScraperStockBR import ScraperStockBr
from .ScraperFII import ScraperFII
from app.model.TickerType import STOCKS_BR_ID, FII_ID

class ScraperConstructor:
    def build(self, type):
        if type == STOCKS_BR_ID:
            return ScraperStockBr(type)
        elif type == FII_ID:
            return ScraperFII(type)
