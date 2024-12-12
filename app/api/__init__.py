from api.auth import router as auth_router
from api.scraper import router as scraper_router
from api.user import router as user_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(scraper_router)