import concurrent.futures

from logger import Logger

from app.model.Ticker import Ticker as TickerModel
from app.model.TickerType import STOCKS_BR_ID, FII_ID
from app.model.ScrapperRun import ScrapperRun as ScrapperRunModel
from app.model.ScrapperRunTicker import ScrapperRunTicker as ScrapperRunTickerModel

from app.repository.Ticker import Ticker as TickerRepository
from app.repository.ScrapperRun import ScrapperRun as ScrapperRunRepository
from app.repository.ScrapperRunTicker import ScrapperRunTicker as ScrapperRunTickerRepository
from app.service.Scrapper.ScrapperConstructor import ScrapperConstructor as  ScrapperConstructorService

MAX_WORKERS = 5

def get_ticker_info(scrapper_run_id, ticker):
    logger = Logger(print_log=True)

    scrapper_run_ticker_repository = ScrapperRunTickerRepository(ScrapperRunTickerModel)
    scrapper_service = ScrapperConstructorService().build(ticker.ticker_type_id)

    scrapper_run_ticker = scrapper_run_ticker_repository.create(
        {
            'scrapper_run_id': scrapper_run_id,
            'ticker_id': ticker.id,
            'started_at': scrapper_run_ticker_repository.get_current_date(),
            'ended_at': None
        }
    )

    logger.print(f"Getting data from {ticker.name}")
    data = scrapper_service.get_data(ticker.name)
    logger.print(data)

    if 'exception' in data:
        exec_failed = True
        cause_exec_failed = data['exception']
    else:
        exec_failed = False
        cause_exec_failed = None

    scrapper_run_ticker_repository.update(
        scrapper_run_ticker.id,
        {
            'ended_at': scrapper_run_ticker_repository.get_current_date(),
            'exec_failed': exec_failed,
            'cause_exec_failed': cause_exec_failed
        }
    )

    return data


def get_invest_data(max_workers):
    ticker_repository = TickerRepository(TickerModel)
    scrapper_run_repository = ScrapperRunRepository(ScrapperRunModel)

    tickers = ticker_repository.all()

    scrapper_run = scrapper_run_repository.create(
        {
            'started_at': scrapper_run_repository.get_current_date(),
            'ended_at': None
        }
    )

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_tickers = None

        for ticker in tickers:
            future_tickers = executor.submit(get_ticker_info, scrapper_run.id, ticker)

        if future_tickers:
            future_info_tickers = future_tickers.result()
    
    scrapper_run_repository.update(
        scrapper_run.id,
        {
            'ended_at': scrapper_run_repository.get_current_date()
        }
    )

def main():
    get_invest_data(max_workers = MAX_WORKERS)

if __name__ == "__main__":
    main()