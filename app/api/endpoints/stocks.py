import os
import requests
from dotenv import load_dotenv
from fastapi import APIRouter, \
    HTTPException
from ..DTO.basemodels import StockData, HistoricalData, StockSearch
load_dotenv()
router = APIRouter()
POLYGON_API_KEY = os.getenv("FINANCIAL_API_KEY")
BASE_URL = "https://api.polygon.io"

@router.get("/stocks")
async def read_items():
    return {"message": "Endpoint works!"}

@router.get("/stocks/{symbol}", response_model=StockData)
async def get_stock_data(symbol: str):
    url = f"{BASE_URL}/v3/reference/tickers/{symbol}?apiKey={POLYGON_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()["results"]
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch stock data")

@router.get("/stocks/{symbol}/historical")
async def get_historical_data(symbol: str, date_from: str, date_to: str, multiplier: int, timespan: str):
    url = f"{BASE_URL}/v2/aggs/ticker/{symbol}/range/{multiplier}/{timespan}/{date_from}/{date_to}?adjusted=true&apiKey={POLYGON_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch historical data")

@router.get("/stocks/search/{query}")
async def search_stocks(query: str):
    url = f"{BASE_URL}/v3/reference/tickers?search={query}&apiKey={POLYGON_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch search results")