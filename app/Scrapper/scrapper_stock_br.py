from .generic import GenericScrapper


class ScrapperStockBr(GenericScrapper):
    def __init__(self, type):
        super().__init__()
        self.url = self.url + "acoes/"
        self.type = type

    def get_data_from_ticker(self, ticker):
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

        data = {
            "ticker": ticker,
            "type": self.type,
            "price": self.convert_to_float(current_value),
            "dy": self.convert_to_float(dy_value),
            "pvp": self.convert_to_float(pvp_value),
            "roe": self.convert_to_float(roe_value),
            "dl_ebitda": self.convert_to_float(dl_ebitda_value),
            "sector": sector,
            "sub_sector": sub_sector,
        }
        return data
