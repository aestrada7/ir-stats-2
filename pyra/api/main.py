from fastapi import FastAPI
from driver import router as driver_router
from fetch import router as fetch_router
from seasons import router as seasons_router
from season_sessions import router as season_sessions_router

from insta import router as insta_router

app = FastAPI()

app.include_router(driver_router)
app.include_router(fetch_router)
app.include_router(seasons_router)
app.include_router(season_sessions_router)

app.include_router(insta_router)