from pydantic import BaseModel

class RunScraper(BaseModel):
    limit : int | None = 1
    max_workers: int | None = 1