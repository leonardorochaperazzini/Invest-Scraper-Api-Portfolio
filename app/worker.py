import concurrent.futures
import time

from .model.Ticker import Ticker as TickerModel
from .model.ScraperRun import ScraperRun as ScraperRunModel
from .model.ScraperRunTicker import ScraperRunTicker as ScraperRunTickerModel
from .model.ScraperTickerData import ScraperTickerData as ScraperTickerDataModel

from .repository.Ticker import Ticker as TickerRepository
from .repository.ScraperRun import ScraperRun as ScraperRunRepository
from .repository.ScraperRunTicker import ScraperRunTicker as ScraperRunTickerRepository
from .repository.ScraperTickerData import ScraperTickerData as ScraperTickerDataRepository

from .service.ScraperRun import ScraperRun as ScraperRunService

MAX_WORKERS = 2
LIMIT = 10

def main():
    max_workers = MAX_WORKERS
    limit = LIMIT

    ticker_repository = TickerRepository(TickerModel)
    scraper_run_repository = ScraperRunRepository(ScraperRunModel)

    invest_service = ScraperRunService(
        scraper_run_repository = scraper_run_repository,
        scraper_run_ticker_repository = ScraperRunTickerRepository(ScraperRunTickerModel),
        scraper_ticker_data_repository =  ScraperTickerDataRepository(ScraperTickerDataModel)
    )

    tickers = ticker_repository.all(limit=limit)

    scraper_run = scraper_run_repository.create(
        {
            'started_at': scraper_run_repository.get_current_date(),
            'ended_at': None
        }
    )

    scraper_drive_is_accessible = True

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for ticker in tickers:
            invest_service = ScraperRunService(
                scraper_run_repository = scraper_run_repository,
                scraper_run_ticker_repository = ScraperRunTickerRepository(ScraperRunTickerModel),
                scraper_ticker_data_repository =  ScraperTickerDataRepository(ScraperTickerDataModel)
            )
            
            scraper_drive_is_accessible = invest_service.check_if_driver_is_accessible()

            if scraper_drive_is_accessible:
                future_ticker = executor.submit(invest_service.scraper_ticker_info, scraper_run.id, ticker)

                def callback(future):
                    scraper_run_ticker_id, ticker_info = future.result()
                    invest_service.save_ticker_info(scraper_run_ticker_id, ticker_info)
                
                future_ticker.add_done_callback(callback)

    scraper_run = scraper_run_repository.update(
        scraper_run.id,
        {
            'ended_at': scraper_run_repository.get_current_date()
        }
    )

    return {"scraper_run": scraper_run.to_dict()}

if __name__ == "__main__":
    main()