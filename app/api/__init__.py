from fastapi import FastAPI
from api.rule.Scraper import RunScraper
from service.Invest import run_invest_scraping_and_save_data
from api.middleware.ScraperTimeout import ScraperTimeout as ScraperTimeoutMiddleware
from api.middleware.HandleError import HandleError as HandleErrorMiddleware

app = FastAPI()

app.add_middleware(ScraperTimeoutMiddleware)
app.add_middleware(HandleErrorMiddleware)

@app.post("/scraper/run")
def run_scraper(item: RunScraper):
    scraper_run = run_invest_scraping_and_save_data(
        max_workers=item.max_workers,
        limit=item.limit
    )
    return {"scraper_run": scraper_run}