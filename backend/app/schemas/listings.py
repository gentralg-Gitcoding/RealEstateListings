from pydantic import BaseModel
from typing import Literal

class Listing (BaseModel):
    id: str
    source: str
    address: str
    city: str
    state: str
    zip: str
    price: float
    bedrooms: int
    bathrooms: float
    sqft: int
    latitude: float
    longitude: float
    listedDate: str
    status: Literal["active", "pending", "sold"]
    description: str

    model_config = {
        "from_attributes": True
    }

class ScoredListing (Listing):
    score: float

class SearchResult(BaseModel):
    data: list[ScoredListing]
    total: int
    page: int
    pageSize: int