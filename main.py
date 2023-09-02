import json
from scrapper.types import STOCKS_BR, FII
from scrapper.scrapper_constructor import ScrapperConstructor
from google_sheet_invest import GoogleSheetInvest


def __call_scrapper(type, tickers, tickers_info):
    scraper = ScrapperConstructor().build(type)

    for ticker in tickers:
        print(f"Getting data from {ticker}")
        data = scraper.get_data(ticker)
        print(data)
        tickers_info.append(data)

    scraper.driver_quit()

    return tickers_info


def get_invest_data():
    tickers_info = []

    tickers = [
        "EGIE3",
        "GGBR4",
        "ITUB4",
        "KLBN11",
        "VALE3",
        "VIVT3",
    ]

    tickers_info = __call_scrapper(STOCKS_BR, tickers, tickers_info)

    tickers = [
        "CPTS11",
        "KNCR11",
        "BRCO11",
        "PVBI11",
        "KNRI11",
        "BCFF11",
        "VISC11",
        "XPML11",
        "BTLG11",
        "HTMX11",
        "HFOF11",
    ]

    tickers_info = __call_scrapper(FII, tickers, tickers_info)

    with open("extractions/data.json", "w") as file:
        json.dump(tickers_info, file, indent=4)


# You need to create a service account on google cloud platform, download the json file and put it on the root folder as service_account_credential.json
# You need share the google sheet with the email on the json file
def save_invest_data_on_google_sheet():
    gs_invest = GoogleSheetInvest()
    gs_invest.save_data(STOCKS_BR)
    gs_invest.save_data(FII)


def main():
    get_invest_data()
    save_invest_data_on_google_sheet()


if __name__ == "__main__":
    main()
