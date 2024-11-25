from logger import Logger

from app.service.Scraper.model.TickerInfo import TickerInfo

from app.service.Scraper.ScraperConstructor import ScraperConstructor as  ScraperConstructorService

class Invest:
    def __init__(self, scraper_run_ticker_repository, print_log = True):
        self.scraper_run_ticker_repository = scraper_run_ticker_repository
        self.logger = Logger(print_log=print_log)
    
    def scraper_ticker_info(self, scraper_run_id, ticker):
        scraper_service = ScraperConstructorService().build(ticker.ticker_type_id)

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
            data = scraper_service.get_data(ticker.name)

            exec_failed = False
            cause_exec_failed = None
        except Exception as e:
            exec_failed = True
            cause_exec_failed = data['exception']

        self.scraper_run_ticker_repository.update(
            scraper_run_ticker.id,
            {
                'ended_at': self.scraper_run_ticker_repository.get_current_date(),
                'exec_failed': exec_failed,
                'cause_exec_failed': cause_exec_failed
            }
        )

        return data
    
    def save_ticker_info(self, ticker_info: TickerInfo):
        print('save_ticker_info(self, scraper_data)')
        print(ticker_info)
        print('save_ticker_info(self, scraper_data)')
        #if 'exception' in scraper_data:
        #    self.logger.print(f"Failed to get data from {scraper_data['ticker_name']}: {scraper_data['exception']}")
        #else:
        #    self.logger.print(f"Data from {scraper_data['ticker_name']} saved successfully")
        #    self.logger.print(scraper_data)
        #    # Save data in database
        #    pass