import json

import concurrent.futures

from contract.repository.Base import Base as BaseRepositoryInterface

from model.Ticker import Ticker as TickerModel
from model.ScraperRun import ScraperRun as ScraperRunModel
from model.ScraperRunTicker import ScraperRunTicker as ScraperRunTickerModel
from model.ScraperTickerData import ScraperTickerData as ScraperTickerDataModel

from repository.Ticker import Ticker as TickerRepository
from repository.ScraperRun import ScraperRun as ScraperRunRepository
from repository.ScraperRunTicker import ScraperRunTicker as ScraperRunTickerRepository
from repository.ScraperTickerData import ScraperTickerData as ScraperTickerDataRepository

from service.Scraper.model.TickerInfo import TickerInfo
from service.Logger import LoggerSingleton as logger_singleton
from service.Scraper.ScraperConstructor import ScraperConstructor as  ScraperConstructorService

class Invest:
    def __init__(self, scraper_run_ticker_repository: BaseRepositoryInterface, scraper_ticker_data_repository: BaseRepositoryInterface):
        self.scraper_run_ticker_repository = scraper_run_ticker_repository
        self.scraper_ticker_data_repository = scraper_ticker_data_repository
    
    def scraper_ticker_info(self, scraper_run_id : int, ticker : TickerModel) -> tuple[int, TickerInfo]:
        scraper_service = ScraperConstructorService().build(ticker.ticker_type_id)

        scraper_run_ticker = self.scraper_run_ticker_repository.create(
            {
                'scraper_run_id': scraper_run_id,
                'ticker_id': ticker.id,
                'started_at': self.scraper_run_ticker_repository.get_current_date(),
                'ended_at': None
            }
        )

        logger_singleton.print(f"Getting data from {ticker.name}")
        try:
            ticker_info = scraper_service.get_data(ticker.name)

            exec_failed = False
            cause_exec_failed = None
        except Exception as e:
            ticker_info = None
            exec_failed = True
            cause_exec_failed = str(e)
            logger_singleton.print(f"Failed to get data from {ticker.name} | cause: {cause_exec_failed}")

        self.scraper_run_ticker_repository.update(
            scraper_run_ticker.id,
            {
                'ended_at': self.scraper_run_ticker_repository.get_current_date(),
                'exec_failed': exec_failed,
                'cause_exec_failed': cause_exec_failed
            }
        )

        return scraper_run_ticker.id, ticker_info 
    
    def save_ticker_info(self, scraper_run_ticker_id: int, ticker_info: TickerInfo = None) -> None:
        if ticker_info is not None:    
            self.scraper_ticker_data_repository.create(
                {
                    'scraper_run_ticker_id': scraper_run_ticker_id,
                    'data': ticker_info.__json__()
                }
            )
            logger_singleton.print(f"Data from {ticker_info.ticker} saved successfully")
            logger_singleton.print(json.dumps(ticker_info.__json__(), indent=4))
        else:
            logger_singleton.print(f"Failed to get data from scrapper run ticker id {scraper_run_ticker_id}")


def run_invest_scraping_and_save_data(max_workers: int, limit: int = None) -> dict:
    ticker_repository = TickerRepository(TickerModel)
    scraper_run_repository = ScraperRunRepository(ScraperRunModel)

    tickers = ticker_repository.all(limit=limit)

    scraper_run = scraper_run_repository.create(
        {
            'started_at': scraper_run_repository.get_current_date(),
            'ended_at': None
        }
    )

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for ticker in tickers:
            scraper_run_ticker_repository = ScraperRunTickerRepository(ScraperRunTickerModel)
            scraper_ticker_data_repository = ScraperTickerDataRepository(ScraperTickerDataModel)
            invest_service = Invest(scraper_run_ticker_repository, scraper_ticker_data_repository)
            future_ticker = executor.submit(invest_service.scraper_ticker_info, scraper_run.id, ticker)

            def callback(future):
                ticker_info, additional_data = future.result()
                invest_service.save_ticker_info(ticker_info, additional_data)
            
            future_ticker.add_done_callback(callback)

    scraper_run = scraper_run_repository.update(
        scraper_run.id,
        {
            'ended_at': scraper_run_repository.get_current_date()
        }
    )

    return scraper_run.to_dict()