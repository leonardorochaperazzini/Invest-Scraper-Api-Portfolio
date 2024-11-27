from retry import retry

from .Generic import GenericScraper

from .model.TickerInfo import TickerInfo

class ScraperStockBr(GenericScraper):
    def __init__(self, type, logger):
        super().__init__(type, logger)
        self.url = self.url + "acoes/" 

    @retry(tries=3, delay=1, jitter=2)
    def get_data_from_ticker(self, ticker):
        url = self.url + ticker

        soup = self.call_url(url)
        soup = self.get_html()

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
            soup.find(
                "div",
                {
                    "title": "Facilita a análise e comparação da relação do preço de negociação de um ativo com seu VPA."
                },
            )
            .find("strong", {"class": "value"})
            .text
        )

        roe_value = (
            soup.find(
                "div",
                {
                    "title": "Mede a capacidade de agregar valor de uma empresa a partir de seus próprios recursos e do dinheiro de investidores."
                },
            )
            .find("strong", {"class": "value"})
            .text
        )

        dl_ebitda_value = (
            soup.find(
                "div",
                {
                    "title": "Indica quanto tempo seria necessário para pagar a dívida líquida da empresa considerando o EBITDA atual. Indica também o grau de endividamento da companhia."
                },
            )
            .find("strong", {"class": "value"})
            .text
        )

        sector = (
            soup.find("span", {"class": "sub-value"}, text="Setor de Atuação")
            .find_parent("div")
            .find("strong", {"class": "value"})
            .text
        )

        sub_sector = (
            soup.find("span", {"class": "sub-value"}, text="Subsetor de Atuação")
            .find_parent("div")
            .find("strong", {"class": "value"})
            .text
        )

        ticker_info = TickerInfo()

        ticker_info.set_ticker(ticker)
        ticker_info.set_price(current_value)
        ticker_info.set_dy(dy_value)
        ticker_info.set_pvp(pvp_value)
        ticker_info.set_roe(roe_value)
        ticker_info.set_dl_ebitda(dl_ebitda_value)
        ticker_info.set_sector(sector)
        ticker_info.set_sub_sector(sub_sector)

        return ticker_info
