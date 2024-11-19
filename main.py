import concurrent.futures
from logger import Logger
from Scrapper.types import STOCKS_BR, FII
from Scrapper.scrapper_constructor import ScrapperConstructor

def get_tickers_info(invest_type, tickers):
    return_tickers = []
    logger = Logger(print_log=True)
    scrapper = ScrapperConstructor().build(invest_type)

    for ticker in tickers:
        logger.print(f"Getting data from {ticker}")
        data = scrapper.get_data(ticker)
        logger.print(data)
        return_tickers.append(data)

    scrapper.driver_quit()

    return return_tickers


def get_tickers_info_concurrently(stock_type, tickers):
    return get_tickers_info(stock_type, tickers)

def get_invest_data(max_workers):
    tickers_stocks = [
        "EGIE3",
        "GGBR4",
        #"ITUB4",
        #"KLBN11",
        #"VALE3",
        #"VIVT3",
    ]

    tickers_fii = [
        "CPTS11",
        #"KNCR11",
        #"BRCO11",
        #"PVBI11",
        #"KNRI11",
        #"BCFF11",
        "VISC11",
        #"XPML11",
        #"BTLG11",
        #"HTMX11",
        #"HFOF11",
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_stocks = executor.submit(get_tickers_info_concurrently, STOCKS_BR, tickers_stocks)
        future_fii = executor.submit(get_tickers_info_concurrently, FII, tickers_fii)

        tickers_info_stocks = future_stocks.result()
        tickers_info_fii = future_fii.result()

def main():
    max_workers = 1
    get_invest_data(max_workers)

if __name__ == "__main__":
    main()