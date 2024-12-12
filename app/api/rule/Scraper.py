from pydantic import BaseModel

class RunScraper(BaseModel):
    limit : int | None = 10
    max_workers: int | None = 2