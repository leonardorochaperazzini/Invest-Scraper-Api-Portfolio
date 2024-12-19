import json

from app.contract.repository.Base import Base as BaseRepositoryInterface

from app.model.Ticker import Ticker as TickerModel
from app.model.TickerType import FII_ID

from app.service.Scraper.model.TickerInfo import TickerInfo
from app.service.Logger import LoggerSingleton as logger_singleton
from app.service.Scraper import ScraperConstructor as  ScraperConstructorService

class ScraperRun:
    def __init__(self, scraper_run_repository: BaseRepositoryInterface = None, scraper_run_ticker_repository: BaseRepositoryInterface = None, scraper_ticker_data_repository: BaseRepositoryInterface = None) -> None:
        self.scraper_run_ticker_repository = scraper_run_ticker_repository
        self.scraper_ticker_data_repository = scraper_ticker_data_repository
        self.scraper_run_repository = scraper_run_repository

    def check_if_driver_is_accessible(self) -> bool:
        scraper_service = ScraperConstructorService().build(FII_ID)
        return scraper_service.check_driver_is_running()
    
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

    def is_scraper_running(self) -> bool:
        scraper_runs = self.scraper_run_repository.get_scrapers_running()
        if len(scraper_runs) > 0:
            return True
        else:
            return False