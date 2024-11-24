from .ScrapperStockBR import ScrapperStockBr
from .ScrapperFII import ScrapperFII
from app.model.TickerType import STOCKS_BR_ID, FII_ID

class ScrapperConstructor:
    def build(self, type):
        if type == STOCKS_BR_ID:
            return ScrapperStockBr(type)
        elif type == FII_ID:
            return ScrapperFII(type)
