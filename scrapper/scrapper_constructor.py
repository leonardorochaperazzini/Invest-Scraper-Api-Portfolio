from .scrapper_stock_br import ScrapperStockBr
from .scrapper_fii import ScrapperFII
from .types import STOCKS_BR, FII


class ScrapperConstructor:
    def build(self, type):
        if type == STOCKS_BR:
            return ScrapperStockBr(type)
        elif type == FII:
            return ScrapperFII(type)
