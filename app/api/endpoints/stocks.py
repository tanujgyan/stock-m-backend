import os
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.database import database, crud, models
from ..DTO.basemodels import StockData, HistoricalData

load_dotenv()
router = APIRouter()
POLYGON_API_KEY = os.getenv("FINANCIAL_API_KEY")
BASE_URL = "https://api.polygon.io"


@router.get("/stocks")
async def read_items():
    return {"message": "Endpoint works!"}


@router.get("/stocks/{symbol}", response_model=StockData)
async def get_stock_data(symbol: str, db: Session = Depends(database.get_db)):
    db_stock = crud.get_stock_by_ticker(db, symbol)
    if db_stock:
        return db_stock
    else:
        url = f"{BASE_URL}/v3/reference/tickers/{symbol}?apiKey={POLYGON_API_KEY}"
        response = requests.get(url)

        if response.status_code == 200 and response.json()["results"]:
            stock_data = response.json()["results"]
            db_stock = crud.create_stock(db, stock_data)
            return db_stock
        else:
            raise HTTPException(
                status_code=response.status_code, detail="Failed to fetch stock data"
            )


@router.get("/stocks/{symbol}/historical", response_model=HistoricalData)
async def get_historical_data(
    symbol: str,
    date_from: str,
    date_to: str,
    multiplier: int,
    timespan: str,
    db: Session = Depends(database.get_db),
):
    try:
        stock = await get_stock_data(symbol, db)
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail="Stock not found")
        else:
            raise

    date_from_obj = datetime.strptime(date_from, "%Y-%m-%d")
    date_to_obj = datetime.strptime(date_to, "%Y-%m-%d")
    results = []
    current_date = date_from_obj
    all_data_exists = True

    while current_date <= date_to_obj:
        db_data = (
            db.query(models.HistoricalStockData)
            .filter(
                models.HistoricalStockData.symbol == symbol,
                models.HistoricalStockData.timestamp == current_date,
            )
            .first()
        )

        if not db_data:
            all_data_exists = False
            break  # Exit the loop if data is missing
        else:
            results.append(
                {
                    "o": db_data.open,
                    "h": db_data.high,
                    "l": db_data.low,
                    "c": db_data.close,
                    "v": db_data.volume,
                    "t": int(db_data.timestamp.timestamp() * 1000),
                }
            )
        current_date += timedelta(days=1)

    if all_data_exists:
        return {
            "ticker": symbol,
            "queryCount": len(results),
            "resultsCount": len(results),
            "adjusted": True,
            "results": results,
            "status": "OK",
            "request_id": "db_fetch",
            "count": len(results),
        }

    else:
        # Fetch missing data from Polygon.io
        url = f"{BASE_URL}/v2/aggs/ticker/{symbol}/range/1/day/{date_from}/{date_to}?adjusted=true&apiKey={POLYGON_API_KEY}"
        response = requests.get(url)

        if response.status_code == 200 and response.json()["results"]:
            historical_data = response.json()
            for result in historical_data["results"]:
                timestamp = datetime.fromtimestamp(result["t"] / 1000)
                if (
                    not db.query(models.HistoricalStockData)
                    .filter(
                        models.HistoricalStockData.symbol == symbol,
                        models.HistoricalStockData.timestamp == timestamp,
                    )
                    .first()
                ):
                    result["symbol"] = symbol
                    result["timestamp"] = timestamp
                    result["open"] = result["o"]
                    result["high"] = result["h"]
                    result["low"] = result["l"]
                    result["close"] = result["c"]
                    result["volume"] = result["v"]
                    crud.create_historical_data(db, result)
            return historical_data
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to fetch historical data",
            )


@router.get("/stocks/search/{query}")
async def search_stocks(query: str):
    url = f"{BASE_URL}/v3/reference/tickers?search={query}&apiKey={POLYGON_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(
            status_code=response.status_code, detail="Failed to fetch search results"
        )
