from .scrapper_stock_br import ScrapperStockBr
from .types import STOCKS_BR


class ScrapperConstructor:
    def build(self, type):
        if type == STOCKS_BR:
            return ScrapperStockBr(type)
