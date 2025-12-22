from pydantic import BaseModel, Field
from typing import Optional, List

class PriceDistribution(BaseModel):
    seller: Optional[str] = Field(description = "The name of the seller or retailer.")
    price: Optional[float] = Field(description = "The price offered by the seller.")


class FetcherOutput(BaseModel):
    product_name: str
    brand: Optional[str] = None
    model: Optional[str] = None
    category: Optional[str] = None
    market_region: Optional[str] = None
    currency: Optional[str] = "USD"
    timestamp: str
    current_price: Optional[float] = None
    lowest_price: Optional[float] = None
    highest_price: Optional[float] = None
    average_price: Optional[float] = None
    seller_count: Optional[int] = 0
    price_distribution: List[PriceDistribution]
    trend_signals: Optional[dict] = None