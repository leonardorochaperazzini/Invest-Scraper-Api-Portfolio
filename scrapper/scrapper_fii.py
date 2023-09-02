from .generic import GenericScrapper


class ScrapperFII(GenericScrapper):
    def __init__(self, type):
        super().__init__()
        self.url = self.url + "fundos-imobiliarios/"
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

        data = {
            "ticker": ticker,
            "type": self.type,
            "price": self.convert_to_float(current_value),
            "dy": self.convert_to_float(dy_value),
            "pvp": self.convert_to_float(pvp_value),
            "segment": segment,
            "type_anbima": type_anbima,
            "segment_anbima": segment_anbima,
        }
        return data
