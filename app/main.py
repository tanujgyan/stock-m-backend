from fastapi import FastAPI

from app.api.endpoints import stocks, watchlist, portfolio, news
from app.database import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(stocks.router)
app.include_router(watchlist.router)
app.include_router(portfolio.router)
app.include_router(news.router)



@app.get("/")
async def root():
    return {"message": "Stock Market Backend API"}