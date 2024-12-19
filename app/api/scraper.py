import concurrent.futures
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from app.api.rule.Scraper import RunScraper

from app.model.Ticker import Ticker as TickerModel
from app.model.ScraperRun import ScraperRun as ScraperRunModel
from app.model.ScraperRunTicker import ScraperRunTicker as ScraperRunTickerModel
from app.model.ScraperTickerData import ScraperTickerData as ScraperTickerDataModel

from app.repository.Ticker import Ticker as TickerRepository
from app.repository.ScraperRun import ScraperRun as ScraperRunRepository
from app.repository.ScraperRunTicker import ScraperRunTicker as ScraperRunTickerRepository
from app.repository.ScraperTickerData import ScraperTickerData as ScraperTickerDataRepository

from app.service.Auth import get_current_active_user
from app.service.Auth.model.User import User as UserModel
from app.service.ScraperRun import ScraperRun as ScraperRunService


router = APIRouter()

@router.post("/scraper/run")
def run_scraper(current_user: Annotated[UserModel, Depends(get_current_active_user)], item: RunScraper):
    max_workers = item.max_workers
    limit = item.limit

    ticker_repository = TickerRepository(TickerModel)
    scraper_run_repository = ScraperRunRepository(ScraperRunModel)

    invest_service = ScraperRunService(
        scraper_run_repository = scraper_run_repository,
        scraper_run_ticker_repository = ScraperRunTickerRepository(ScraperRunTickerModel),
        scraper_ticker_data_repository =  ScraperTickerDataRepository(ScraperTickerDataModel)
    )
    
    scraper_is_running = invest_service.is_scraper_running()
    if scraper_is_running:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Scraper is already running"
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

    if scraper_drive_is_accessible:
        return {"scraper_run": scraper_run.to_dict()}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Scraper remote driver failed to connect"
        )

    