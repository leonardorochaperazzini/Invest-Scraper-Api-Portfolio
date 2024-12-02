from fastapi import FastAPI

from api.rule.scraper import RunScraper

from service.Invest import run_invest_scraping_and_save_data

app = FastAPI()

@app.post("/scraper/run")
def run_scraper(item: RunScraper):
    scraper_run = run_invest_scraping_and_save_data(
        max_workers = item.max_workers,
        limit = item.limit
    )

    return {"scraper_run": scraper_run}
