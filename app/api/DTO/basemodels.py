from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from app.api.DTO.marketenums import MarketEnum


class StockData(BaseModel):
    ticker: str
    name: str
    market: MarketEnum
    locale: str
    primary_exchange: str
    type: str
    active: bool
    currency_name: str
    cik: Optional[str]
    composite_figi: Optional[str]
    share_class_figi: Optional[str]
    last_updated_utc: datetime


class HistoricalData(BaseModel):
    ticker: str
    queryCount: int
    resultsCount: int
    adjusted: bool
    results: List[dict]
    status: str
    request_id: str
    count: int


class StockSearch(BaseModel):
    results: List[StockData]
    count: int
    status: str
    request_id: str
