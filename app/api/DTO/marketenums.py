from enum import Enum

class MarketEnum(str, Enum):
     STOCKS = "stocks"
     CRYPTO = "crypto"
     FX = "fx"
     OTC = "otc"
     INDICIES = "indices"