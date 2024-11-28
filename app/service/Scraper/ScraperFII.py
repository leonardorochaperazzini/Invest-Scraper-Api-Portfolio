from retry import retry

from .Generic import GenericScraper

from .model.TickerInfo import TickerInfo

class ScraperFII(GenericScraper):
    def __init__(self):
        super().__init__()
        self.url = self.url + "fundos-imobiliarios/"

    @retry(tries=3, delay=1, jitter=2)
    def get_data_from_ticker(self, ticker : str) -> TickerInfo:
        url = self.url + ticker

        soup = self.call_url(url)

        current_value = (
            soup.find("div", {"title": "Valor atual do ativo"})
            .find("strong", {"class": "value"})
            .text
        )

        dy_value = (
            soup.find("div", {"title": "Dividend Yield com base nos últimos 12 meses"})
            .find("strong", {"class": "value"})
            .text
        )

        pvp_value = (
            soup.find("h3", {"class": "title m-0"}, text="P/VP")
            .find_parent("div")
            .find("strong", {"class": "value"})
            .text
        )

        segment = (
            soup.find("span", {"class": "sub-value"}, text="Segmento")
            .find_parent("div")
            .find("strong", {"class": "value"})
            .text
        )

        type_anbima = (
            soup.find("h3", {"class": "title m-0"}, text="Tipo ANBIMA")
            .find_parent("div")
            .find("strong", {"class": "value"})
            .text
        )

        segment_anbima = (
            soup.find("h3", {"class": "title m-0"}, text="Segmento ANBIMA")
            .find_parent("div")
            .find("strong", {"class": "value"})
            .text
        )

        ticker_info = TickerInfo()

        ticker_info.set_ticker(ticker)
        ticker_info.set_price(current_value)
        ticker_info.set_dy(dy_value)
        ticker_info.set_pvp(pvp_value)
        ticker_info.set_segment(segment)
        ticker_info.set_type_anbima(type_anbima)
        ticker_info.set_segment_anbima(segment_anbima)

        return ticker_info
