import json

from logger import Logger

from app.model.Ticker import Ticker

from app.service.Scraper.model.TickerInfo import TickerInfo

from app.service.Scraper.ScraperConstructor import ScraperConstructor as  ScraperConstructorService

class Invest:
    def __init__(self, scraper_run_ticker_repository, scraper_ticker_data_repository, print_log : bool = True):
        self.scraper_run_ticker_repository = scraper_run_ticker_repository
        self.scraper_ticker_data_repository = scraper_ticker_data_repository
        self.logger = Logger(print_log=print_log)
    
    def scraper_ticker_info(self, scraper_run_id : int, ticker : Ticker):
        scraper_service = ScraperConstructorService().build(ticker.ticker_type_id, self.logger)

        scraper_run_ticker = self.scraper_run_ticker_repository.create(
            {
                'scraper_run_id': scraper_run_id,
                'ticker_id': ticker.id,
                'started_at': self.scraper_run_ticker_repository.get_current_date(),
                'ended_at': None
            }
        )

        self.logger.print(f"Getting data from {ticker.name}")
        try:
            ticker_info = scraper_service.get_data(ticker.name)

            exec_failed = False
            cause_exec_failed = None
        except Exception as e:
            ticker_info = None
            exec_failed = True
            cause_exec_failed = str(e)

        self.scraper_run_ticker_repository.update(
            scraper_run_ticker.id,
            {
                'ended_at': self.scraper_run_ticker_repository.get_current_date(),
                'exec_failed': exec_failed,
                'cause_exec_failed': cause_exec_failed
            }
        )

        return scraper_run_ticker.id, ticker_info 
    
    def save_ticker_info(self, scraper_run_ticker_id: int, ticker_info: TickerInfo = None):
        if ticker_info is not None:    
            self.scraper_ticker_data_repository.create(
                {
                    'scraper_run_ticker_id': scraper_run_ticker_id,
                    'data': ticker_info.__json__()
                }
            )
            self.logger.print(f"Data from {ticker_info.ticker} saved successfully")
            self.logger.print(json.dumps(ticker_info.__json__(), indent=4))
        else:
            self.logger.print(f"Failed to get data from scrapper run ticker id {scraper_run_ticker_id}")