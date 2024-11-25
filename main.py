import concurrent.futures

from app.model.Ticker import Ticker as TickerModel
from app.model.TickerType import STOCKS_BR_ID, FII_ID
from app.model.ScraperRun import ScraperRun as ScraperRunModel
from app.model.ScraperRunTicker import ScraperRunTicker as ScraperRunTickerModel

from app.repository.Ticker import Ticker as TickerRepository
from app.repository.ScraperRun import ScraperRun as ScraperRunRepository
from app.repository.ScraperRunTicker import ScraperRunTicker as ScraperRunTickerRepository

from app.service.Invest import Invest as InvestService

MAX_WORKERS = 5
PRINT_LOG = True

def run_invest_scraping_and_save_data(max_workers, print_log):
    ticker_repository = TickerRepository(TickerModel)
    scraper_run_repository = ScraperRunRepository(ScraperRunModel)

    tickers = ticker_repository.all()

    scraper_run = scraper_run_repository.create(
        {
            'started_at': scraper_run_repository.get_current_date(),
            'ended_at': None
        }
    )

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for ticker in tickers:
            scraper_run_ticker_repository = ScraperRunTickerRepository(ScraperRunTickerModel)
            invest_service = InvestService(scraper_run_ticker_repository, print_log)
            future_ticker = executor.submit(invest_service.scraper_ticker_info, scraper_run.id, ticker)
            future_ticker.add_done_callback(lambda future: invest_service.save_ticker_info(future.result()))
    
    scraper_run_repository.update(
        scraper_run.id,
        {
            'ended_at': scraper_run_repository.get_current_date()
        }
    )

def main():
    run_invest_scraping_and_save_data(
        max_workers = MAX_WORKERS,
        print_log = PRINT_LOG
    )

if __name__ == "__main__":
    main()